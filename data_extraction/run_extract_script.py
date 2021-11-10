from data_extraction.factory_extractors import FactoryExtractors

if __name__=='__main__':

    extract = FactoryExtractors
    transfer = extract.get_concrete('fbref')
    transfer_ = extract.get_concrete('transfermrkt')

    test = transfer.extract_data(persist_data = True)
    print(1)

