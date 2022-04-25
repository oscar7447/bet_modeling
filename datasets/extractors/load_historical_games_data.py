import pandas as pd

class LoadHistoricalGamesData():
    """
    
    Interface for loading historical data, 
    this is to make seamless the data source changes
    
    
    """

    def load_data()-> pd.DataFrame:
        df = pd.read_pickle('files/match_historical_data_v3.pkl')
        return df
        