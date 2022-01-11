from factory.abstract_factory import AbstractFactory
from features.calculation.match_win_loss import match_win_loss
from features.calculation.probs_end_season import ProbsEndSeason

class FeatureFactory(AbstractFactory):

    def get_concrete(extractor_name):
    

        feature_extractors = {
            
            "match_win_loss": match_win_loss,
            "probs end season": ProbsEndSeason
   
        }
        
        return feature_extractors[extractor_name]
 
