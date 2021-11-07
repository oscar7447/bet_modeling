from data_extraction.extract_from_transfermrkt import data_from_transfermrkt
from data_extraction.extract_historical_match_data import get_data_fbref
from abstract_factory import AbstractFactory


class FactoryExtractors(AbstractFactory):
    """
    Factory method to get the different data extractors used in the system
    """
    def get_concrete(extractor_name):
    

        data_extractors = {
            
            "transfermrkt": data_from_transfermrkt,
            "fbref": get_data_fbref
   
        }
        
        return data_extractors[extractor_name]
    