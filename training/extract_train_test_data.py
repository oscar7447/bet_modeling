import numpy as np
import pandas as pd
from datasets.extractors.load_historical_games_data import LoadHistoricalGamesData

class ExtractTrainTestData:
    _keys = ['home_team', 'away_team', 'competition', 'date', 'matchweek']


    def get_train_test_data(self, season_init:str, 
                            season_end:str, 
                            competition:str)->pd.DataFrame:

        """
        Gets the train or test data and put in the correct format from historical 
        games data
        """

        games_df = LoadHistoricalGamesData.load_data()
        tmp_games_df = games_df[(games_df['season']>=season_init)&
                                (games_df['season']<season_end)&
                                (games_df['comp']==competition)]
        
        
        tmp_games_df['home_team'] = np.where(tmp_games_df['venue']=='Home', 
                                            tmp_games_df['team_name'], 
                                            tmp_games_df['opponent'])
        tmp_games_df['away_team'] = np.where(tmp_games_df['venue']=='Away', 
                                            tmp_games_df['team_name'], 
                                            tmp_games_df['opponent'])
        
        tmp_games_df.rename(columns={'comp':'competition', 'time':'date'}, inplace=True)

        tmp_games_df['matchweek'] = tmp_games_df['round'].str.split(' ', expand=True)[1]
        tmp_games_df['matchweek'] = tmp_games_df['matchweek'].astype(int)
        
        tmp_games_df.drop_duplicates(inplace=True)
        return tmp_games_df[self._keys]