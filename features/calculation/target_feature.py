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
       
        """
        n_previous_matches = 10
        home_df = pd.DataFrame()
        away_df = pd.DataFrame()

        for _, i in df_games.iterrows():
            
            la_liga_df_tmp =  la_liga_df[((la_liga_df['team_name']== i['away_team']) & \
                            (la_liga_df['opponent']== i['home_team'])) | \
                            ((la_liga_df['team_name']== i['home_team']) &
                            (la_liga_df['opponent']== i['away_team']))]


        return la_liga_df_tmp