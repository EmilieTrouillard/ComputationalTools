import pickle
import os
from readGraph import readPickled
from utilities import HOME_DIR

### =================
### HELPERS
### =================

def removeSingleQuotes(title):
    '''
    Single Quotes cannot be used for data in the neo4j database.
    '''
    L = title.split('"')
    if len(L)>0 and len(L)%2 ==0:
        return "'".join(title.split('"'))
    else: return title

### =================
from indexcreation_mapReduce import ID_TO_TITLE_FILENAME
from graphcreation_mapReduce import GRAPH_FILENAME

# FILES
NODES_CSV_FILENAME = HOME_DIR + '/sample/nodes_wikilinks.csv'
RELATIONSHIPS_CSV_FILENAME = HOME_DIR + '/sample/relationships_wikilinks.csv'


nodes = open(NODES_CSV_FILENAME, 'w')
nodes.write('pageId:ID(Page);title\n')

pages = readPickled(ID_TO_TITLE_FILENAME)
nodes.write('\n'.join([';'.join([str(key), str(value).replace('"', "''").replace(';', ',')]) for key, value in pages.items()]))
nodes.close()

relationships = open(RELATIONSHIPS_CSV_FILENAME, 'w')
relationships.write(':START_ID(Page);:END_ID(Page)\n')

graph = open(GRAPH_FILENAME, 'r')
out = []
for line in graph:
    data = line[:-1].split(' ')
    if len(data) > 0:
        origin = data[0]
        data = data[1:]
        out.append('\n'.join([';'.join([origin, target]) for target in data if origin != target]))

relationships.write('\n'.join(out))
relationships.close()
