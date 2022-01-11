import os
import pandas as pd


def cache_disk_dataframes(dirname):

    def func_wrapper(func):

        def wrapper(*args, **kwargs):
            filename = [str(i[1]) for i in kwargs.items() 
                        if (type(i[1]) is str) 
                        or (type(i[1]) is float) 
                        or (type(i[1]) is int)]
            filename = '_'.join(filename).replace(' ','_').lower()
            filename = 'df_'+filename+'.pkl'

            if os.path.exists(dirname):
                files_list = os.listdir(dirname)
                if filename not in files_list:
                    probs = func(*args, **kwargs)
                    probs.to_pickle(dirname+'/'+filename)
                elif filename in files_list:
                    probs = pd.read_pickle(dirname+'/'+filename)
            else:
                os.mkdir(dirname)
                probs = func(*args, **kwargs)
                probs.to_pickle(dirname+'/'+filename)

            return probs
        return wrapper
    return func_wrapper

            