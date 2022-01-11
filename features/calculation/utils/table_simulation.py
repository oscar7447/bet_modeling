import pandas as pd
import numpy as np


def table_simulation(df_matches:pd.DataFrame(), competition:str, season:str, matchweek:int):
    """
       Calculates the posicion table for a given 
       matchweek, competition and season.


    Args:
        df_matches (pd.DataFrame): Dataframe of previous matches
        competition (str): Competition to be simulated
        season (str): Season to be calculated
        matchweek (int): Game count of the season (Generally from 1 to 38)
    """


    df_matches = df_matches[df_matches['comp']==competition]
    season_df = df_matches[df_matches['season']==season]

    season_df['matchweek'] = [season_df['round'].str.split(' ') \
                            .iloc[i][1]  for i in range(len(season_df))]
    season_df['matchweek'] = season_df['matchweek'].astype(int)
    season_df = season_df[season_df['matchweek']<matchweek]

    grouped = season_df.groupby(['team_name','result']).count()[['time']].reset_index()

    grouped['points'] = np.where(grouped['result']=='W'
                                , grouped['time']*3
                                , np.where(grouped['result']=='D'
                                , grouped['time'], 0))

    posicion_table = grouped.groupby(['team_name'])[['points']].sum() \
                    .sort_values(by='points', ascending=False).reset_index()
    posicion_table['posicion'] = posicion_table.reset_index()['index']+1

    return posicion_table
