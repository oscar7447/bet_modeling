import pandas as pd

class LoadHistoricalBetsData():
    """
    
    Interface for loading historical data, 
    this is to make seamless the data source changes
    
    
    """

    def load_data()-> pd.DataFrame:
        df = pd.read_pickle('files/betdata.pkl')
        return df
        