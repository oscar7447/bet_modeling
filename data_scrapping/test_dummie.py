from general_utils.enums.teams_enums import LaligaTeamEnums
from general_utils.enums.datasource_enums import DataSourceEnum
import numpy as np
import pandas as pd
import unidecode
if __name__=='__main__':
    transer_ = pd.read_pickle('files/transfer_information.pkl')
    matchhistorical = pd.read_pickle('files/match_historical_data.pkl')
    transer_.rename(columns={'club_name':'team_name'}, inplace=True)

    matchhistorical['team_name'] = matchhistorical['team_name'].apply(lambda x: unidecode.unidecode(x))
    matchhistorical['opponent'] = matchhistorical['opponent'].apply(lambda x: unidecode.unidecode(x))
    transer_['team_name'] = transer_['team_name'].astype(str).apply(lambda x: unidecode.unidecode(x))

    matchhistorical['team_name'] = matchhistorical['team_name'].str.replace('-', ' ').str.replace('_', ' ')
    matchhistorical['opponent'] = matchhistorical['opponent'].str.replace('-', ' ').str.replace('_', ' ')
    transer_['team_name'] = transer_['team_name'].str.replace('-', ' ').str.replace('_', ' ')

    for i in LaligaTeamEnums:

        matchhistorical['team_name'] = matchhistorical['team_name'].apply(lambda x: unidecode.unidecode(x))

        matchhistorical['team_name'] = np.where(matchhistorical['team_name']==i[DataSourceEnum.fbref]
                                        , i['name']
                                        , matchhistorical['team_name'])
        matchhistorical['opponent'] = np.where(matchhistorical['opponent']==i[DataSourceEnum.fbref]
                                        , i['name']
                                        , matchhistorical['opponent'])

        transer_['team_name'] = np.where(transer_['team_name']==i[DataSourceEnum.transfermarket]
                                        , i['name']
                                        , transer_['team_name'])

    print(1)
    transer_.to_pickle('files/transfer_information_v3.pkl')
    matchhistorical.to_pickle('files/match_historical_data_v3.pkl')


