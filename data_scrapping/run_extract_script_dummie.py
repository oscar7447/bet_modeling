import pandas as pd
from data_extraction.extractor_factory import FactoryExtractors
if __name__=='__main__':

    extract = FactoryExtractors
    transfer = extract.get_concrete('fbref')
    transfer_ = extract.get_concrete('transfermrkt')

    test = transfer_.extract_data(persist_data = True)
    d = pd.read_pickle('files/transfer_information.pkl')
    print(1)

