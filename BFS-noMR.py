import sys
from numpy import inf

input_file = "temp/input.txt"


class Node():

    def __init__(self,id):
        self._id = id

    def setadjacencylist(self,adjacencylist):

        self._adjacencylist = adjacencylist

class BFS_noMR:

    def __init__(self,nodes):
        self._nodes = nodes
        self._n = len(nodes)

    def shortestpath(self,startnode):

        dist = [inf for i in range(0,self._n)]
        prev = [None for i in range(0,self._n)]
        visited = [False for i in range(0,self._n)]
        path = [[] for i in range(0,self._n)]

        visited[startnode._id] = True
        dist[startnode._id] = 0
        path[startnode._id] = [startnode._id]

        d = 0
        curqueue = [startnode]
        nextqueue = []
        curpath = []

        while len(curqueue) > 0:
            d += 1
            for node in curqueue:
                curpath = path[node._id]
                for neighbor in node._adjacencylist:
                    if not visited[neighbor._id]:
                        visited[neighbor._id] = True
                        dist[neighbor._id] = d
                        prev[neighbor._id] = node._id
                        path[neighbor._id] = curpath.copy()
                        path[neighbor._id].append(neighbor._id)
                        nextqueue.append(neighbor)
            curqueue = nextqueue
            nextqueue = []
        return dist,path

def initializenodes():

    nodes = []
    adjacencylist_id_all = []

    with open(input_file) as f:
        for line in f.readlines():
            adjacencylist_id_all.append([])
            x = line.split(" ")
            id = int(x[0])
            adjacencylist_id = []
            node = None
            for i in range(1,len(x)):
                adjacencylist_id.append(int(x[i]))
            adjacencylist_id_all[id] = adjacencylist_id
            node = Node(id)
            nodes.append(node)
            f.close()

    for node in nodes:
        adjacencylist = []
        for id in adjacencylist_id_all[node._id]:
            adjacencylist.append(nodes[id])
        node.setadjacencylist(adjacencylist)

    return nodes

if __name__ == "__main__":

    startnode_id = int(sys.argv[1])

    nodes = initializenodes()

    bfs = BFS_noMR(nodes)
    dist,path = bfs.shortestpath(nodes[startnode_id])
    for i in range(0,len(dist)):
        print("dist = " + str(dist[i]))
        print("path = " + str(path[i]))
