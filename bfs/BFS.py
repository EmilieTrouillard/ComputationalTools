'''
STANDARD IMPLEMENTATION OF SHORTEST PATH THROUGH BFS.
INPUT:
* Graph Input file: The input file should consist of lines of the form: <node_id> <neighbor_id1,neighbor_id2,...,neighbor_idk>. The ID's should be 0,1,...,n-1.
* Start Node : ID of the start nodeself.
* (OPT) End Node : ID of the end node. If this is not provided, the program finds the paths to all the nodes.

RUN BFS.py -h to learn more about the arguments and options

OUTPUT:
---
'''
import sys
from numpy import inf
import argparse
from utilities import readPickled

class Node():

    def __init__(self,id):
        self._id = id

    def setadjacencylist(self,adjacencylist):

        self._adjacencylist = adjacencylist

class BFS():

    def __init__(self,nodes):
        self._nodes = nodes
        self._n = len(nodes)

    def getPath(self,startnode_id,endnode_id,prev):

        nid = endnode_id
        path = [nid]
        while nid != startnode_id:
            if nid == None:
                return []
            nid = prev[nid]
            path.append(nid)

        path.reverse()
        return path

    def shortestpath(self,startnode, *endnode):

        dist = [inf for i in range(0,self._n)]
        prev = [None for i in range(0,self._n)]
        visited = [False for i in range(0,self._n)]

        visited[startnode._id] = True
        dist[startnode._id] = 0

        d = 0
        curqueue = [startnode]
        nextqueue = []

        distances = [0 for i in range (0,100)]
        distances[0] = 1
        nInf = 0

        while len(curqueue) > 0:
            d += 1
            for node in curqueue:
                for neighbor in node._adjacencylist:
                    if not visited[neighbor._id]:
                        visited[neighbor._id] = True
                        dist[neighbor._id] = d
                        prev[neighbor._id] = node._id
                        distances[d] += 1
                        if len(endnode) == 1 and endnode[0]._id == neighbor._id:
                            return d, [d], [self.getPath(startnode._id, endnode[0]._id, prev)]
                        nextqueue.append(neighbor)
            curqueue = nextqueue
            nextqueue = []

        for di in dist:
            if di==inf:
                nInf += 1

        # Is that needed ?

        # print(distances)
        # print(sum(distances[9:]))
        # print(nInf)
        # print(sum(distances)+nInf)
        # print(self._n)

        path = []
        for i in range (0,self._n):
            path.append(self.getPath(startnode._id,self._nodes[i]._id,prev))

        return d-1,dist,path

def initializenodes(input_file):

    nodes_id = []
    adjacencylist_id_all = []

    with open(input_file) as f:
        line = f.readline()

        while line:
            x = line.strip().split(" ")
            id = int(x[0])
            nodes_id.append(id)
            adjacencylist_id = []
            for i in range(1,len(x)):
                adjacencylist_id.append(int(x[i]))
            adjacencylist_id_all.append(adjacencylist_id)
            line = f.readline()

    nodes = [None for i in range(0,len(nodes_id))] # nodes sorted wrt. id

    for i in range(0,len(nodes_id)):
        id = nodes_id[i]
        node = Node(id)
        nodes[id] = node

    for i in range(0,len(nodes_id)):
        id = nodes_id[i]
        adjacencylist = []
        for neighbor_id in adjacencylist_id_all[i]:
            adjacencylist.append(nodes[neighbor_id])
        nodes[id].setadjacencylist(adjacencylist)


    return nodes

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Graph input file. FORMAT: Node NeighborNode1 NeighborNode2 ...")
    parser.add_argument("-si", "--startnode_id", help="ID of the start node (As seen in the graph input file). REQUIRED if startnode name is not given", type=int)
    parser.add_argument("-ei", "--endnode_id", help="ID of the end node (As seen in the graph input file). If not given, will compute the shortest path to all nodes.", type=int)
    parser.add_argument("-sn", "--startnode_name", help="Name of the start article. If a mapping title to id is given (ti), replaces the startnode id option.")
    parser.add_argument("-en", "--endnode_name", help="Name of the end node. As for the start node, a mapping title to id (ti) is required.")
    parser.add_argument("-ti", "--titles_to_ids", help="Option to allow to input the article titles instead of their ids. Must be the file name that contains the dictionary title to id")
    parser.add_argument("-it", "--ids_to_titles", help="Option to allow to output the article titles instead of their ids. Must be the file name that contains the dictionary id to title")
    args = parser.parse_args()

    input_file = args.input_file

    # CHECK ON INPUT NODES VALIDITY
    if not (args.startnode_id == None or args.startnode_name == None):
        sys.exit('You need to specify a start node! Run python bfs/BFS.py -h for help.')
    if args.startnode_name and not args.titles_to_ids:
        sys.exit('If you want to input the start node with its article title you need to provide a title to id file! Run python bfs/BFS.py -h for help.')
    if args.endnode_name and not args.titles_to_ids:
        sys.exit('If you want to input the end node with its article title you need to provide a title to id file! Run python bfs/BFS.py -h for help.')

    # INPUT ARE IDS
    startnode_id, endnode_id = None, None
    if args.startnode_id != None:
        startnode_id = args.startnode_id
    if args.endnode_id != None:
        endnode_id = args.endnode_id

    # INPUT ARE NAMES
    titleToId = None
    if args.titles_to_ids != None:
        titleToId = readPickled(args.titles_to_ids)
        startnode_id = int(titleToId[args.startnode_name])

    if args.startnode_name != None:
        startnode_id = int(titleToId[args.startnode_name])
    if args.endnode_name != None:
        endnode_id = int(titleToId[args.endnode_name])

    # ID TO TITLE
    idToTitle = None
    if args.ids_to_titles != None:
        idToTitle = readPickled(args.ids_to_titles)


    nodes = initializenodes(input_file)
    bfs = BFS(nodes)

    if endnode_id != None:
        d,dist,path = bfs.shortestpath(nodes[startnode_id], nodes[endnode_id])
        if idToTitle != None:
            pathTitles = [idToTitle[str(idPath)] for idPath in path[0]]
            print("Distance: " + str(dist[0]) + ". Path: " + str(pathTitles))
        else:
            print("Distance: " + str(dist[0]) + ". Path: " + str(path[0]))
    else:
        d,dist,path = bfs.shortestpath(nodes[startnode_id])
        for i in range(0,len(dist)):
            if idToTitle != None:
                pathTitles = [idToTitle[str(idPath)] for idPath in path[i]]
                print("Node '" + idToTitle[str(i)] + "'. Distance: " + str(dist[i]) + ". Path: " + str(pathTitles))
            else:
                print("Node " + str(i) + ". Distance: " + str(dist[i]) + ". Path: " + str(path[i]))
