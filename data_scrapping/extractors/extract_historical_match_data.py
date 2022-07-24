from bs4 import BeautifulSoup
import requests
import pandas as pd
from data_extraction.utils.constants import historical_years, codes_fbref
import numpy as np
import unidecode
from abstract_extract import data_extraction
import pickle
from general_utils.enums.datasource_enums import DataSourceEnum


class GetDataFbref(data_extraction):

    @staticmethod
    def preprocess_names(list_names):
        """
        Get a list of names in this case the fisrt letter 
        in capital and drop accents and fill spaces with '-'
        
        """
        drop_accents = np.vectorize(unidecode.unidecode)
        list_names = drop_accents(list_names)
        list_names = [i.replace(' ','-') if len(i.split(' '))>1 else i for i in list_names ]
        
        return list_names


    def extract_data(persist_data:bool):
        """
        
        Extract from fbref.com the results from previous mathces of previous
        seasons 
        

        """
        _use_columns = ['team_name','time', 'comp', 'round', 'dayofweek'
                , 'venue', 'result', 'goals_for', 'goals_against'
                , 'opponent', 'possession','season']

        all_teams = pd.DataFrame()
        for team_name in codes_fbref.keys():
            not_found = []
            all_df = pd.DataFrame()
            for i in range(len(historical_years)):

                if i<len(historical_years)-1:
                    URL = "https://fbref.com/en/squads/"+codes_fbref[team_name]+"/" \
                    +str(historical_years[i])+"-"+str(historical_years[i+1])+"/"+team_name+"-Stats"
                    
                    page = requests.get(URL)
                    soup = BeautifulSoup(page.content, "html.parser")
                    try:
                        a = soup.find_all("table")[1]
                    except:
                        name = str(team_name)+'_'+str(historical_years[1])+"-"+str(historical_years[1+1])
                        not_found.append(name)                
                        continue
                        
                    new_table = pd.DataFrame(index=[0]) 
                    df= pd.DataFrame(index=[0]) 

                    row_marker = 0
                    for row in a.find_all('tr'):
                        columns = row.find_all('td')
                        for column in columns:
                            le = len(column.get_text())
                            addd = column.get_text()
                            if le==0:
                                addd = 0

                            new_table[column.get('data-stat')] = str(addd)
                        new_table['time'] = row.find_all('th')[0].get_text()
                        df = pd.concat([new_table, df])
                    df['season'] = str(historical_years[i])+"-"+str(historical_years[i+1])
                    all_df = pd.concat([all_df, df])
            all_df.columns = all_df.columns.str.lower()
            all_df['team_name'] = team_name
            all_df.dropna(subset=['comp'], inplace=True)

            all_teams = pd.concat([all_teams, all_df[_use_columns]])
            all_teams = data_extraction.standardize_names(all_teams, DataSourceEnum.fbref)







        if persist_data:
            with open('/files/match_historical_data.pkl', 'wb') as f:
                pickle.dump(object, f)

        return all_teams, not_found

