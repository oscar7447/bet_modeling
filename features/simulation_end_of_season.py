import pandas as pd
import numpy as np
from features.table_simulation import table_simulation

def simulation_end_season(df_matches, competition, season, current_matchweek):


    """ 
        Function that simulates the final table of the season and
        returns the probabilites of the team to end in top 5, end as a champion or 
        in relegation zone

    Args:
        df_matches ([type]): Dataframe containing the historical information 
        competition ([type]): Competition that the calculation is going to be made.
        season ([type]): 
        current_matchweek ([type]): Matchweek from 1 to the end of the season(generally 38)

    Returns:
        [type]: [description]
    """
    
    points_vector = [0, 1, 3]
    prob_vector = [1/3, 1/3, 1/3]
    total_matches = 38
    sims = 5000

    remaining_matches = total_matches+1-current_matchweek
    season_df = df_matches[df_matches['season']==season]
    season_df = season_df[season_df['comp']==competition]

    season_df['matchweek'] = [season_df['round'].str.split(' ') \
                            .iloc[i][1]  for i in range(len(season_df))]

    season_df['matchweek'] = season_df['matchweek'].astype(int)
    #season_df[season_df['matchweek']>=current_matchweek]
    if current_matchweek==1:
        season_points = np.random.choice(points_vector, remaining_matches)
    elif current_matchweek>1:
        
        table = table_simulation(df_matches, competition, season, current_matchweek)
        season_points = np.random.choice(points_vector, remaining_matches)
    for j in range(sims):
        table['tmp_points'] = np.zeros(len(table))
        for i in range(len(table)):

            season_points = np.random.choice(points_vector, remaining_matches)
            table['tmp_points'].iloc[i] = table['points'].iloc[i]+season_points.sum()
        
        
        table.sort_values(by='tmp_points', ascending=False, inplace=True)
        table['posicion_tmp_'+str(j)] = np.linspace(1, len(table), len(table))


    table.drop(columns=['points', 'posicion', 'tmp_points'], inplace=True)
    tmp = table.T.reset_index()
    tmp.columns = tmp[tmp['index']=='team_name'].values[0]
    tmp.drop([0], inplace=True)
    tmp = tmp.drop(columns='team_name').apply(lambda x: x.value_counts())
    tmp = tmp/sims
    probs_top5 = tmp.loc[1:5].sum()
    probs_descenso = tmp[tmp.shape[0]-2:tmp.shape[0]].sum()
    probs_champion = tmp.loc[1]

    return probs_top5, probs_descenso, probs_champion