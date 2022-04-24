import pandas as pd
import numpy as np
from features.abstract_feature import AbstractFeature

class TransferData(AbstractFeature):



    _entities = ['home_team', 'away_team', 'season' \
                    , 'date', 'competition', 'matchweek']
    _keys_away = ['away_team', 'date']
    _keys_home = ['home_team', 'date']

    def calculate(df:pd.DataFrame, df_games:pd.DataFrame)->pd.DataFrame: 
        
        """

        Args:
            name (str): [Name of the team to calculate]
            date_match (str): [Date of the calculation (match to be play)]
            n_previous_matches (int): [Number of previous matches to take into account]
            la_liga_df (DataFrame): [DataFrame of raw matches information from fbref]
        """

        ## Transformation of season column. Eventually move it to the scrapping function
        transfer = pd.read_pickle('files/transfer_information_v3.pkl')
        transfer['season'] = transfer['season'].str.split('/') 
        transfer = transfer[transfer.isna().sum(axis=1)==0]
        transfer.reset_index(drop=True, inplace=True)

        for j, row in transfer.iterrows():
            tmp = np.array(row['season']).astype(int)
            converted = [i+2000 if i<30 else i+1900 for i in tmp]
            converted = pd.Series([np.array(converted).astype(str)]).str.join('-')
            transfer['season'].iloc[j] = converted[0]
        
        #########################################################



        ### Get the correct data 
        transfer.drop_duplicates(['team_name','season'], inplace=True)
        feature_columns = ['number_of_loans', 'number_of_free_transfers',
                            'total_amount', 'team_name', 'season']
        home = df_games.merge(transfer[feature_columns], 
                        left_on=['home_team', 'season'],
                        right_on=['team_name', 'season'])
        home.rename(columns={'number_of_loans':'number_of_loans_home',
                            'number_of_free_transfers':'number_of_free_transfers_home',
                            'total_amount':'total_amount_home'
                            }, inplace=True)
        away = df_games.merge(transfer[feature_columns], 
                        left_on=['away_team', 'season'],
                        right_on=['team_name', 'season'])

        away.rename(columns={'number_of_loans':'number_of_loans_away',
                            'number_of_free_transfers':'number_of_free_transfers_away',
                            'total_amount':'total_amount_away'
                            }, inplace=True)

        merge_cols = ['home_team', 'away_team', 'season', \
                     'date', 'competition', 'matchweek']

        df = away.merge(home, on=merge_cols)                           

        return df