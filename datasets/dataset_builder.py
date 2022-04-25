import pandas as pd
from features.feature_factory import FeatureFactory
from datasets.game_dataset import game_dataset_builder
from datasets.extractors.load_historical_games_data import LoadHistoricalGamesData
if __name__=='__main__':
#[TODO] PASS DF FOR EACH GAME WITH THE BASIC INFO: HOME-AWAY TEAM, MATCHWEEK, SEASON, COMPETITION 
    keys = ['home_team', 'away_team', 'season'
            , 'date', 'competition', 'matchweek']
    matchhistorical = LoadHistoricalGamesData.load_data()
    df_games = game_dataset_builder()
    features =  FeatureFactory

    ff = features.get_concrete('target variable').calculate(
                matchhistorical, 
                df_games
                )
    df = df_games.merge(features.get_concrete('transfer information')\
                        .calculate(matchhistorical, df_games), 
                        on=keys, 
                        how='left')

    df = df.merge(features.get_concrete('match win loss')\
                        .calculate(matchhistorical, df_games), 
                        on=keys, 
                        how='left')
    df = df.merge(features.get_concrete('match win loss same team')\
                        .calculate(matchhistorical, df_games), 
                        on=keys, 
                        how='left')                         
    
    df = df.merge(features.get_concrete('probs end season')\
                            .calculate(matchhistorical, df_games)\
                            , on=keys, how='left')

    a = pd.read_pickle('files/betdata.pkl')
    print(1)