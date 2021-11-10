from data_extraction.extract_from_transfermrkt import GetDataTransfermarket
from data_extraction.extract_historical_match_data import GetDataFbref
from abstract_factory import AbstractFactory


class FactoryExtractors(AbstractFactory):
    """
    Factory method to get the different data extractors used in the system
    """
    def get_concrete(extractor_name):
    

        data_extractors = {
            
            "transfermrkt": GetDataTransfermarket,
            "fbref": GetDataFbref
   
        }
        
        return data_extractors[extractor_name]
    