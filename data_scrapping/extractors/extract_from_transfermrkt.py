from bs4 import BeautifulSoup
import requests
import pandas as pd
from data_extraction.utils.constants import codes_transfermrkt
import numpy as np
import unidecode
from abstract_extract import data_extraction
import re
from general_utils.datasource_enums import DataSourceEnum

class GetDataTransfermarket(data_extraction):
    """[summary]

    Args:
        data_extraction ([type]): [description]
    """
    @staticmethod
    def codes_generation(season_init = 2002, season_end = 2021):
        """
        Generate codes and club names for URL generation
        """
        teams_links={}

        teams_season = pd.DataFrame([])
        teams_season['name'] = []
        teams_season['codes'] = []
        for season_id in range(season_init, season_end):
            URL = str("https://www.transfermarkt.com/laliga/startseite/wettbewerb/ES1/plus/?saison_id="+str(season_id))
            headers = {"User-Agent":"Mozilla/5.0"}
            page = requests.get(URL, headers= headers)
            soup = BeautifulSoup(page.content, "html.parser")


            rows = 0
            soup = soup.findAll("table")[12]
            links = set([search.get("href") for search in soup.findAll("a")])
            teams_links[str(season_id)] = links
            teams = [i.split('/')[1] for i in teams_links[str(season_id)] if len(i)>10]
            codes = [i.split('/')[4] for i in teams_links[str(season_id)] if len(i)>10]
            tmp_teams = pd.DataFrame(list(zip(teams, codes)), columns=['name', 'codes'])
            teams_season = pd.concat([tmp_teams, teams_season], ignore_index=True)
            teams_season.drop_duplicates(inplace=True)
        return teams_season

    def extract_data(self, persist_data:bool):

        """
        Extract historical transfer data from transfermarkt.com 
        that contains, arrivals, departures, money invested and money spent

        Returns:
            [persist_data]: [True or False if you want to save the dataframe]
        """

        all_clubs = pd.DataFrame(index=[0]) 
        codes_transfermrkt = self.codes_generation()
        for _, i in codes_transfermrkt.iterrows():
            URL = "https://www.transfermarkt.com/"+str(i['name'])+"/alletransfers/verein/"+str(i['codes'])
            headers = {"User-Agent":"Mozilla/5.0"}
            page = requests.get(URL, headers= headers)
            soup = BeautifulSoup(page.content, "html.parser")

            new_table = pd.DataFrame(index=[0]) 
            col_names = ['name', 'drop', 'from_to', 'value']

            all_df = pd.DataFrame(index=[0]) 
            for k in range(len(soup.find_all(class_ = 'box'))):
                df= pd.DataFrame(index=[0]) 
                table = soup.find_all(class_ = 'box')[k].select('table')
                if soup.find_all(class_ = 'box')[k].select('h2') and table:
                    type_table = soup.find_all(class_ = 'box')[k].select('h2')[0].text.strip('\n').strip(' ').split(' ')[0]
                    season_table = soup.find_all(class_ = 'box')[k].select('h2')[0].text.strip('\n').strip(' ').split(' ')[1]


                    for row in table[0].find_all('tr'):
                        column_marker = 0
                        columns = row.find_all('td')
                        if len(columns)==1:
                            continue
                        for column in columns:
                            le = len(column.get_text())
                            addd = column.get_text()
                            if le==0:
                                addd = 0
                            new_table[col_names[column_marker]] = str(addd)
                            column_marker =column_marker + 1
                        df = pd.concat([new_table, df])
                    df.dropna(inplace=True)
                    df.drop(columns=['drop'], inplace=True)
                    ## get season and arrival or departure
                    df['type'] = type_table
                    df['season'] = season_table
                    ## get value
                    a = [(re.findall(r'[0-9]+', df['value'].iloc[i])) for i in range(len(df))]
                    df['value_money'] = ['.'.join(a[i]) for i in range(len(a))]

                    df['value_money'] = np.where(df['value_money']=='', 0, df['value_money'])
                    df['value_money'] = df['value_money'].astype(float)

                    df['multiplier'] = np.where(df['value'].str.endswith('m')
                                                , 1e6
                                                , np.where(df['value'].str.endswith('Th.'), 1e3,0))

                    df['value_money'] = df['multiplier']*df['value_money']
                    df['number_of_loans'] = df['value'].str.lower().str.contains('loan').sum()
                    df['number_of_free_transfers'] = df['value'].str.lower().str.contains('free').sum()
                    df['total_amount'] = df['value_money'].sum()
                    all_df = pd.concat([df, all_df])
                else:
                    continue
                
                
            all_df['team_name'] = i['name']
            
            all_clubs = pd.concat([all_df, all_clubs])
            all_clubs = data_extraction.standardize_names(all_clubs, DataSourceEnum.transfermarket)
        if persist_data:
            all_clubs.to_pickle("files/transfer_information.pkl")

        return all_clubs

