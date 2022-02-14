import pandas as pd


def game_dataset_builder():
        game = {'home_team':['atletico_madrid','real_madrid'],
            'away_team':['barcelona', 'barcelona'],
            'season':['2019-2020','2019-2020'],
            'date':  ['2020-06-12', '2020-07-12'],
            'competition':['La Liga','La Liga'],
            'matchweek':[30, 31]
    }

        #current_data = pd.read_pickle('files/match_historical_data_v2.pkl')
        
        game_df = pd.DataFrame(game, index=[0,1])
        return game_df

