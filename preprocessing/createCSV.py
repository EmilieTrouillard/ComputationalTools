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

def removeSingleQuotes(title):
    L = title.split('"')
    if len(L)>0 and len(L)%2 ==0:
        return "'".join(title.split('"'))
    else: return title


# FILES
NODES_CSV = 'nodesCleanTitles.csv'
RELATIONSHIPS_CSV = 'relationships_unique.csv'
GRAPH = 'preprocessing/graphfile_global_MergedRedirect_NoDuplicate'
ID_TO_TITLE = 'preprocessing/idtotitlemapNoRedirect'


nodes = open(NODES_CSV, 'w')
nodes.write('pageId:ID(Page);title\n')

pages = readPickled(ID_TO_TITLE)
nodes.write('\n'.join([';'.join([str(key), str(value).replace('"', "''").replace(';', ',')]) for key, value in pages.items()]))
nodes.close()

relationships = open(RELATIONSHIPS_CSV, 'w')
relationships.write(':START_ID(Page);:END_ID(Page)\n')

graph = open(GRAPH, 'r')
out = []
for line in graph:
    data = line[:-1].split(' ')
    if len(data) > 0:
        origin = data[0]
        data = data[1:]
        out.append('\n'.join([';'.join([origin, target]) for target in data if origin != target]))

relationships.write('\n'.join(out))
relationships.close()
