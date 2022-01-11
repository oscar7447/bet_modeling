import os

if __name__=='__main__':
    t = os.listdir('cache')
    a = os.path.exists('cache')
    os.mkdir('cache')