from features.feature_factory import FeatureFactory
import pandas as pd
from datasets.game_dataset import game_dataset_builder
if __name__=='__main__':
#[TODO] PASS DF FOR EACH GAME WITH THE BASIC INFO: HOME-AWAY TEAM, MATCHWEEK, SEASON, COMPETITION 
    keys = ['home_team', 'away_team', 'season'
            , 'date', 'competition', 'matchweek']
    matchhistorical = pd.read_pickle('files/match_historical_data_v3.pkl')
    df_games = game_dataset_builder()
    features =  FeatureFactory

    df = df_games.merge(features.get_concrete('match win loss same team')\
                        .calculate(matchhistorical, df_games), 
                        on=keys, 
                        how='left')

    df = df.merge(features.get_concrete('match win loss')\
                        .calculate(matchhistorical, df_games), 
                        on=keys, 
                        how='left')                       
    
    df = df.merge(features.get_concrete('probs end season')\
                            .calculate(matchhistorical, df_games)\
                            , on=keys, how='left')


    print(1)