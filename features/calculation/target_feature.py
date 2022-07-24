import pandas as pd
import numpy as np
from features.calculation.utils.calculation_win_loss_percentage import calculation_win_loss_percentage
from features.abstract_feature import AbstractFeature

class TargetVariable(AbstractFeature):



    _entities = ['home_team', 'away_team', 'season' \
                    , 'date', 'competition', 'matchweek']
    _keys_away = ['away_team', 'date']
    _keys_home = ['home_team', 'date']

    def calculate(la_liga_df:pd.DataFrame, df_games:pd.DataFrame): 
        
        """
        Get the target variable, in this case, the target variable is calculated
        with respect home venue, for example:
            - If away loss, the home win. If away win the home loss. So, the three 
            variables will be: home_win, home_loss, draw
        """
        
        la_liga_df['home_team'] = np.where(la_liga_df['venue']=='Home', 
                                            la_liga_df['team_name'], 
                                            la_liga_df['opponent'])
        la_liga_df['away_team'] = np.where(la_liga_df['venue']=='Away', 
                                            la_liga_df['team_name'], 
                                            la_liga_df['opponent'])
        
        la_liga_df.rename(columns={'comp':'competition', 'time':'date'}, inplace=True)

        la_liga_df['matchweek'] = la_liga_df['round'].str.split(' ', expand=True)[1]
        la_liga_df['matchweek'] = la_liga_df['matchweek'].astype(int)
        cols = list(df_games.columns)
        la_liga_df['y_value'] = np.where((la_liga_df['team_name']==la_liga_df['home_team'])
                                        &(la_liga_df['result']=='L'), 
                                            'home_loss',
                                np.where(
                                    (la_liga_df['team_name']==la_liga_df['away_team'])
                                    &(la_liga_df['result']=='L'), 
                                    'home_win',  
                                np.where(
                                    (la_liga_df['team_name']==la_liga_df['away_team'])
                                    &(la_liga_df['result']=='W'), 
                                    'home_loss',
                                np.where(
                                    (la_liga_df['team_name']==la_liga_df['home_team'])
                                    &(la_liga_df['result']=='W'), 
                                    'home_win', 'draw'))))

        df = la_liga_df[cols+['y_value']].merge(df_games, on = cols)


        return df.drop_duplicates()