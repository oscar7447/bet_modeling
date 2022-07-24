import pandas as pd
from features.feature_factory import FeatureFactory
from datasets.game_dataset import game_dataset_builder
from datasets.extractors.load_historical_games_data import LoadHistoricalGamesData
from general_utils.enums.competitions_enums import CompetitionEnum
from training.extract_train_test_data import ExtractTrainTestData
from general_utils.enums.stage_enumns import StageEnum

if __name__=='__main__':
#[TODO] PASS DF FOR EACH GAME WITH THE BASIC INFO: HOME-AWAY TEAM, MATCHWEEK, SEASON, COMPETITION 
    keys = ['home_team', 'away_team', 'season'
            , 'date', 'competition', 'matchweek']
    stage = StageEnum.train
    competition = CompetitionEnum.laliga
    matchhistorical = LoadHistoricalGamesData.load_data()
    matchhistorical = matchhistorical[matchhistorical['comp']==competition]


    #df_games = game_dataset_builder()

    df_games = ExtractTrainTestData().get_train_test_data('2005-2006', 
                                                        '2006-2007',
                                                        CompetitionEnum.laliga)
    features =  FeatureFactory()
    
    features.get_concrete('probs end season')\
                            .calculate(matchhistorical, df_games)
                            

    
    """
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


    if stage in [StageEnum.train, StageEnum.test]:
                df = df.merge(features.get_concrete('target variable').calculate(
                                                        matchhistorical, 
                                                        df_games
                                                        ) , on=keys, how='left')
                

                """
    a = pd.read_pickle('files/betdata.pkl')
    print(1)