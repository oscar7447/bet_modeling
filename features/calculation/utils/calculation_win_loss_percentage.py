import pandas as pd
import numpy as np   
    
    
def calculation_win_loss_percentage(la_liga_df:pd.DataFrame, 
                                    team_name:str, 
                                    date:str, 
                                    n_previous_matches:int,
                                    competition=None)-> pd.DataFrame:

    """
    Creates the win-loss-draw total and percentage of n previous matches

    Args:
        team_name (str): [Name of the team to calculate]
        date (str): [Date of the calculation (match to be play)]
        n_previous_matches (int): [Number of previous matches to take into account]
        la_liga_df (DataFrame): [DataFrame of raw matches information from fbref]
        """
    results = pd.DataFrame(columns=['number_of_draw', 'number_of_loss', 'number_of_win'
                    , 'number_of_draw_away', 'number_of_draw_home', 'number_of_loss_away'
                    , 'number_of_loss_home', 'number_of_loss_neutral', 'number_of_win_away'
                    , 'number_of_win_home', 'number_of_win_neutral'], index=[0])
    
    if competition != None:
        la_liga_df = la_liga_df[la_liga_df['comp']==competition]

    
    la_liga_df.sort_values('time', ascending=False, inplace=True)
    matches = la_liga_df[(la_liga_df['team_name']==team_name)
                        &(la_liga_df['time']<date)].head(n_previous_matches)

    matches['new_result'] = np.where(matches['result']=='W', 'number_of_win'
                            , np.where(matches['result']=='L', 'number_of_loss'
                            , np.where(matches['result']=='D', 'number_of_draw', 'None')))

    ### Previous matches win, loss and draw by venue (home, away)
    win_loss = matches.groupby(['new_result','venue']).count().T.iloc[[0]]
    win_loss.columns = [str(i[0])+'_'+str(i[1]) for i in win_loss.columns]
    win_loss.columns = win_loss.columns.str.lower()
    win_loss.reset_index(drop=True, inplace=True)

    ### Previous matches win, loss total
    win_loss_all = matches.groupby(['new_result']).count().T.iloc[[0]]
    win_loss_all.reset_index(drop=True, inplace=True)
    win_loss = pd.concat([win_loss_all,win_loss], axis=1)
    results.fillna(win_loss, inplace=True)
    results.fillna(0, inplace=True)

    ### percentages
    results['percentage_win'] = results['number_of_win']/n_previous_matches
    results['percentage_loss'] = results['number_of_loss']/n_previous_matches
    results['percentage_draw'] = results['number_of_draw']/n_previous_matches

    number_of_home_games = results['number_of_win_home']+results['number_of_loss_home']+results['number_of_draw_home']
    results['percentage_home_win'] = results['number_of_win_home']/number_of_home_games
    results['percentage_home_loss'] = results['number_of_loss_home']/number_of_home_games
    results['percentage_home_draw'] = results['number_of_draw_home']/number_of_home_games

    number_of_away_games = results['number_of_win_away']+results['number_of_loss_away']+results['number_of_draw_away']
    results['percentage_away_win'] = results['number_of_win_away']/number_of_away_games
    results['percentage_away_loss'] = results['number_of_loss_away']/number_of_away_games
    results['percentage_away_draw'] = results['number_of_draw_away']/number_of_away_games
    results['team_name'] = team_name
    results['date'] = date

    return results