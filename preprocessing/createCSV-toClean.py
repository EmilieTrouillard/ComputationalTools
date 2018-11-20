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

"""nodes = open('nodesCleanTitles.csv', 'w')
nodes.write('pageId:ID(Page);title\n')

pages = readPickled('preprocessing/idtotitlemapNoRedirect')
#nodes.write('\n'.join([';'.join([str(key), removeSingleQuotes(value)]) for key, value in pages.items()]))
nodes.write('\n'.join([';'.join([str(key), str(value).replace('"', "''").replace(';', ',')]) for key, value in pages.items()]))
nodes.close()"""

relationships = open('relationships_unique.csv', 'w')
relationships.write(':START_ID(Page);:END_ID(Page)\n')
#Relationships = open('relationshipsRest.csv', 'w')
#Relationships.write('node1node2\n')
graph = open('preprocessing/graphfile_global_MergedRedirect_NoDuplicate', 'r')
out = []
for line in graph:
    data = line[:-1].split(' ')
    if len(data) > 0:
        origin = data[0]
        data = data[1:]
        out.append('\n'.join([';'.join([origin, target]) for target in data if origin != target]))
#outsmall = out[:10]
#outrest = out[10:]
relationships.write('\n'.join(out))
relationships.close()

#Relationships.write('\n'.join(outrest))
#Relationships.close()