

from data_extraction.factory_extractors import FactoryExtractors
#from data_extraction.extract_from_transfermrkt import data_from_transfermrkt
if __name__=='__main__':

    extract = FactoryExtractors()
    transfer = extract.get_concrete(a = 'fbref')
    transfer_ = extract.get_concrete(a = 'transfermrk')

    test = transfer.extract_data(persist_data = True)
    transfer_.extract_data
    print(1)

# [TODO] ADD IMPORTS ABSOLUTE PATH
# [TODO] ADD GIT IGNORE