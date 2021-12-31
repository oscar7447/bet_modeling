from general_utils.teams_enums import LaligaTeamEnums
from general_utils.datasource_enums import DataSourceEnum
import numpy as np
import pandas as pd

if __name__=='__main__':
    transer_ = pd.read_pickle('files/transfer_information.pkl')
    matchhistorical = pd.read_pickle('files/match_historical_data.pkl')
    transer_.rename(columns={'club_name':'team_name'}, inplace=True)
    for i in LaligaTeamEnums:
        matchhistorical['team_name'] = np.where(matchhistorical['team_name']==i[DataSourceEnum.fbref]
                                        , i['name']
                                        , matchhistorical['team_name'])


        transer_['team_name'] = np.where(transer_['team_name']==i[DataSourceEnum.transfermarket]
                                        , i['name']
                                        , transer_['team_name'])

    print(1)
    transer_.to_pickle('files/transfer_information_v2.pkl')
    matchhistorical.to_pickle('files/match_historical_data_v2.pkl')


