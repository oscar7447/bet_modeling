from bs4 import BeautifulSoup
import requests
import pandas as pd
from data_extraction.constants import codes_transfermrkt
import numpy as np
import unidecode
from abstract_extract import data_extraction


class data_from_transfermrkt(data_extraction):
    """[summary]

    Args:
        data_extraction ([type]): [description]
    """

    def code_generation():
        """
        Generate codes and club names for URL generation
        """
        pass

    def extract_data(persist_data:bool):

        """
        Extract historical transfer data from transfermarkt.com 
        that contains, arrivals, departures, money invested and money spent

        Returns:
            [persist_data]: [True or False if you want to save the data frame]
        """


        all_clubs = pd.DataFrame(index=[0]) 

        for i in codes_transfermrkt.keys():
            URL = "https://www.transfermarkt.com/"+str(i)+"/alletransfers/verein/"+str(codes_transfermrkt[i])
            headers = {"User-Agent":"Mozilla/5.0"}
            page = requests.get(URL, headers= headers)
            soup = BeautifulSoup(page.content, "html.parser")

            new_table = pd.DataFrame(index=[0]) 
            col_names=['name', 'drop', 'from_to', 'value']

            row_marker = 0
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
                
                
            all_df['club_name'] = i
            
            all_clubs = pd.concat([all_df, all_clubs])

            if persist_data:
                all_clubs.to_pickle("files/transfer_information.pkl")

            return all_clubs

