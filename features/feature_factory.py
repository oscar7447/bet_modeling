from factory.abstract_factory import AbstractFactory
from features.calculation.match_win_loss import MatchWinLoss
from features.calculation.probs_end_season import ProbsEndSeason
from features.calculation.match_win_loss_same_team import MatchWinLossMatch
from features.calculation.transfer_feature import TransferData


class FeatureFactory(AbstractFactory):

    def get_concrete(extractor_name): 
    

        feature_extractors = {
            
            "match win loss": MatchWinLoss,
            "probs end season": ProbsEndSeason,
            "match win loss same team": MatchWinLossMatch,
            "transfer information": TransferData
   
        }
        
        return feature_extractors[extractor_name]
 
