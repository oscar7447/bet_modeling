from bs4 import BeautifulSoup
import requests
import pandas as pd
from data_extraction.constants import historical_years, codes_fbref
import numpy as np
import unidecode
from abstract_extract import data_extraction



class get_data_fbref(data_extraction):
    def __init__(self, team_name):
        self.team_name = team_name

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


    def extract_data(self, historical_years, persist_data:bool):
        """
        
        Extract from fbref.com the results from previous mathces of previous
        seasons 
        

        """
        not_found = []
        all_df = pd.DataFrame()
        for i in range(len(historical_years)):

            if i<len(historical_years)-1:
                URL = "https://fbref.com/en/squads/"+codes_fbref[self.team_name]+"/" \
                +str(historical_years[i])+"-"+str(historical_years[i+1])+"/"+self.team_name+"-Stats"
                
                print(URL)
                page = requests.get(URL)
                soup = BeautifulSoup(page.content, "html.parser")
                try:
                    a = soup.find_all("table")[1]
                except:
                    name = str(self.team_name)+'_'+str(historical_years[1])+"-"+str(historical_years[1+1])
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
        all_df['team_name'] = self.team_name
        all_df.dropna(subset=['comp'], inplace=True)
        
        cols = ['team_name','time', 'comp', 'round', 'dayofweek'
                , 'venue', 'result', 'goals_for', 'goals_against'
                , 'opponent', 'possession','season']

        if persist_data:
            all_df[cols].to_pickle('files/match_historical_data.pkl')

        return all_df[cols], not_found

