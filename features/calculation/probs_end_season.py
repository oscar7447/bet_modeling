from features.calculation.utils.simulation_end_of_season import simulation_end_season
from features.abstract_feature import AbstractFeature
class ProbsEndSeason(AbstractFeature):


    def calculate(df_matches, df_games):

        
        tmp_df = df_games[['season', 'matchweek', 'competition']].drop_duplicates()
        for _, i in tmp_df.iterrows():
            probs = simulation_end_season(df_matches = df_matches
                                        , competition = i['competition']
                                        , season = i['season']
                                        , matchweek = i['matchweek'])




        return probs



                                