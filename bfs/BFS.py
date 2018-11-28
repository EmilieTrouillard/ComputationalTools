import sys
from numpy import inf

## To run this program the user must give the path of an input file as the first inputself.
##The input file should consist of lines of the form: <node_id> <neighbor_id1,neighbor_id2,...,neighbor_idk>. The ID's should be 0,1,...,n-1.
## The second argument should be the ID of the start nodeself.
## The third argument should be the ID of the end node. If this is not provided, the program finds the paths to all the nodes.

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

        print(distances)
        print(sum(distances[9:]))
        print(nInf)
        print(sum(distances)+nInf)
        print(self._n)



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

    input_file = sys.argv[1]
    startnode_id = int(sys.argv[2])

    nodes = initializenodes(input_file)
    bfs = BFS(nodes)

    if len(sys.argv) > 3:
        endnode_id = int(sys.argv[3])
        d,dist,path = bfs.shortestpath(nodes[startnode_id], nodes[endnode_id])
        print("Distance: " + str(dist[0]) + ". Path: " + str(path[0]))
    else:
        d,dist,path = bfs.shortestpath(nodes[startnode_id])
        #for i in range(0,len(dist)):
        #    print("Node " + str(i) + ". Distance: " + str(dist[i]) + ". Path: " + str(path[i]))

        print("Max distance: " + str(d))
