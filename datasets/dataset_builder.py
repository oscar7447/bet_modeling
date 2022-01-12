from features.feature_factory import FeatureFactory
import pandas as pd
from datasets.game_dataset import game_dataset_builder
if __name__=='__main__':
#[TODO] PASS DF FOR EACH GAME WITH THE BASIC INFO: HOME-AWAY TEAM, MATCHWEEK, SEASON, COMPETITION 

    matchhistorical = pd.read_pickle('files/match_historical_data_v2.pkl')
    df_games = game_dataset_builder()
    features =  FeatureFactory
    probs_end_season = features.get_concrete('probs end season')
    a = probs_end_season.calculate(matchhistorical, df_games)