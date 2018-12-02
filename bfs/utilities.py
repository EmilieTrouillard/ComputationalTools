'''
UTILITIES FOR BFS
'''
import pickle
import os

HOME_DIR = '/'.join(os.path.dirname(os.path.realpath(__file__)).replace('\\','/').split('/')[:-1])

def readPickled(fileName):
    pickledData = {}
    try:
        if os.path.getsize(fileName) > 0:      
            with open(fileName, "rb") as f:
                unpickler = pickle.Unpickler(f)
                # if file is not empty scores will be equal
                # to the value unpickled
                pickledData = unpickler.load()
    except FileNotFoundError:
        print('FILE NOT FOUND!: {0}'.format(fileName))
        pass
    return pickledData