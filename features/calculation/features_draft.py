import pandas as pd
import numpy as np
from features.calculation.utils.table_simulation import table_simulation



if __name__=='__main__':
    transfer = pd.read_pickle('files/transfer_information_v3.pkl')
    transfer['season'] = transfer['season'].str.split('/') 

    ### FINISH MERGE WITH TRANSFER DF IT HAS ALL THE VARIABLES ALREADY CONSTRUCTED
   # list(map(int, transfer['season'].str.split('/').iloc[0]))
    #transfer[['season']].apply(lambda x: [i+2000 if i>50 else i+1900 for i in list(map(int, x))])
    transfer = transfer[transfer.isna().sum(axis=1)==0]
    transfer.reset_index(drop=True, inplace=True)

    for j, row in transfer.iterrows():
        tmp = np.array(row['season']).astype(int)
        converted = [i+2000 if i>50 else i+1900 for i in tmp]
        converted = pd.Series([np.array(converted).astype(str)]).str.join('-')
        transfer['season'].iloc[j] = converted[0]
    print(1)

