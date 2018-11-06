import pickle
import os


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
        pass
    return pickledData

# TESTABLE
if __name__ == '__main__':
    print('Enter the name of the file that contains the graph:')
    graphFile = input()
    
    print(readPickled(graphFile))
