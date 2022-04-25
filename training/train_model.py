from training.extract_train_test_data import ExtractTrainTestData
from general_utils.competitions_enums import CompetitionEnum
if __name__=='__main__':
    season_train_init = '2002-2003'
    season_train_end = '2016-2017'
    season_test_init = '2016-2017'
    season_test_end = '2020-2021'
    competition = CompetitionEnum.laliga.value

    extractor = ExtractTrainTestData()

    df_train = extractor.get_train_test_data('2002-2003', 
                                            '2016-2017', 
                                            competition)

    df_test = extractor.get_train_test_data('2016-2017', 
                                            '2020-2021', 
                                            competition)

    #[TODO] add Y value and enums inference train etc
    print(1)

