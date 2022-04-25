import pandas as pd

class LoadTransferData():
    """
    
    Interface for loading  data, 
    this is to make seamless the data source changes
    
    
    """

    def load_data()-> pd.DataFrame:
        df = pd.read_pickle('files/transfer_information_v3.pkl')
        return df
        