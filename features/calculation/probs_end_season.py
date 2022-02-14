from tokenize import Triple
from features.calculation.utils.simulation_end_of_season import simulation_end_season
from features.abstract_feature import AbstractFeature
import pandas as pd

class ProbsEndSeason(AbstractFeature):


    def calculate(df_matches: pd.DataFrame, df_games:pd.DataFrame)->pd.DataFrame:

        """
        Calculates the probability of ending in the top 5, champion and descenso

        """

        home_df = pd.DataFrame()
        away_df = pd.DataFrame()

        tmp_df = df_games[['season', 'matchweek', 'competition']].drop_duplicates()
        for _, i in tmp_df.iterrows():
            probs = simulation_end_season(df_matches = df_matches
                                        , competition = i['competition']
                                        , season = i['season']
                                        , matchweek = i['matchweek'])

            probs.reset_index(inplace=True)
            probs.rename(columns={'index':'team_name'}, inplace=True)
            probs['competition'] = i['competition']
            probs['season'] = i['season']
            probs['matchweek'] = i['matchweek']
            probs.fillna(0, inplace=True)

            tmp_home = df_games.merge(probs, left_on=['home_team', 'competition', 'season','matchweek']
                                , right_on=['team_name', 'competition', 'season','matchweek']
                                , how='left').dropna()

            tmp_away = df_games.merge(probs, left_on=['away_team', 'competition', 'season','matchweek']
                    , right_on=['team_name', 'competition', 'season','matchweek']
                    , how='left').dropna()
            if len(home_df) == 0:
                home_df = pd.DataFrame(columns=tmp_home.columns)
                away_df = pd.DataFrame(columns=tmp_away.columns)

            home_df = pd.concat([tmp_home, home_df], axis=0)
            away_df = pd.concat([tmp_away, away_df], axis=0)

        home_df.rename(columns={'probs_top_5':'probs_top_5_home',
                                'probs_champion':'probs_champion_home',
                                'probs_descenso':'probs_descenso_home'
                                }, inplace=True)

        away_df.rename(columns={'probs_top_5':'probs_top_5_away',
                            'probs_champion':'probs_champion_away',
                            'probs_descenso':'probs_descenso_away'
                            }, inplace=True)


        df_games = df_games.merge(home_df, left_on=['home_team', 'away_team'
                                        , 'season', 'date'
                                        , 'competition', 'matchweek']                                   
                                , right_on=['home_team', 'away_team'
                                        ,'season', 'date'
                                        , 'competition', 'matchweek'], how='left').drop(columns='team_name')

        df_games = df_games.merge(away_df
                    , left_on=['home_team', 'away_team'
                                , 'season', 'date', 'competition', 'matchweek']
                    , right_on=['home_team', 'away_team','season'
                                , 'date', 'competition', 'matchweek']
                                , how='left').drop(columns='team_name')
        return df_games



                                