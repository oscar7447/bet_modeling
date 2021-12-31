from abc import ABC, abstractmethod
import enum
import numpy as np
from general_utils.teams_enums import LaligaTeamEnums
class data_extraction(ABC):
 
    @abstractmethod
    def extract_data(self):
        pass


    def standardize_names(df, data_source:enum):
        """Converts the names of different data sources into a standard one

        Args:
            df ([Dataframe]): DF containing the scrapped information
            data_source (str): name of the datasource

        Returns:
            [type]: [description]
        """
        for i in LaligaTeamEnums:
            df['team_name'] = np.where(df['team_name']==i[data_source]
                                        , i['name']
                                        , df['team_name'])

        return df



