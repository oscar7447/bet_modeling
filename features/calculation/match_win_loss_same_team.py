import pandas as pd
import numpy as np
from features.calculation.utils.calculation_win_loss_percentage import calculation_win_loss_percentage
from features.abstract_feature import AbstractFeature

class MatchWinLossMatch(AbstractFeature):



    __entities__ = ['home_team', 'away_team', 'season' \
                    , 'date', 'competition', 'matchweek']
    __keys_away__ = ['away_team', 'date']
    __keys_home__ = ['home_team', 'date']
    __output_signature__ = []

    def calculate(la_liga_df:pd.DataFrame, df_games:pd.DataFrame): 
        
        """
        Creates the win-loss-draw total and percentage of n (10) previous matches

        Args:
            name (str): [Name of the team to calculate]
            date_match (str): [Date of the calculation (match to be play)]
            n_previous_matches (int): [Number of previous matches to take into account]
            la_liga_df (DataFrame): [DataFrame of raw matches information from fbref]
        """
        n_previous_matches = 10
        home_df = pd.DataFrame()
        away_df = pd.DataFrame()

        for _, i in df_games.iterrows():
            
            la_liga_df_tmp =  la_liga_df[((la_liga_df['team_name']== i['away_team']) & \
                            (la_liga_df['opponent']== i['home_team'])) | \
                            ((la_liga_df['team_name']== i['home_team']) &
                            (la_liga_df['opponent']== i['away_team']))]


            home_df_tmp = calculation_win_loss_percentage(la_liga_df_tmp
                                                    , i['home_team']
                                                    , i['date']
                                                    , n_previous_matches
                                                    , i['competition'])

            home_df_tmp.columns = [i+str('_home_same_team') if i not in ('team_name', 'date') \
                                    else i for i in home_df_tmp.columns ]
            home_df = pd.concat([home_df, home_df_tmp])
            

            away_df_tmp = calculation_win_loss_percentage(la_liga_df_tmp
                                                    , i['away_team']
                                                    , i['date']
                                                    , n_previous_matches
                                                    , i['competition'])

            away_df_tmp.columns = [i+str('_away_same_team') if i not in ('team_name', 'date') \
                                    else i for i in away_df_tmp.columns]

            away_df = pd.concat([away_df, away_df_tmp])


        df_games = df_games.merge(home_df
                        , left_on=['home_team','date']
                        , right_on=['team_name','date']
                        , how='left').drop(columns=['team_name'])


        df_games = df_games.merge(away_df
                        , left_on=['away_team','date']
                        , right_on=['team_name','date']
                        , how='left').drop(columns=['team_name'])
                        
        return df_games