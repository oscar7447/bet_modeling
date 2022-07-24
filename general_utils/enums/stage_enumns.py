from enum import Enum

class StageEnum(str, Enum):
    train = 'train'
    test = 'test'
    inference = 'inference'