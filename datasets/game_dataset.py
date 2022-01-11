import pandas as pd


def game_dataset_builder():

    game = {'home_team':['atletico de madrid','real madrid'],
            'away_team':['barcelona', 'barcelona'],
            'season':['2019-2020','2019-2020'],
            'matchweek':  [10,8],
            'competition':['La Liga','La Liga']
    }


    game_df = pd.DataFrame(game, index=[0,1])
    return game_df

