import mrjob
from mrjob.job import MRJob
from numpy import inf

## The user should set the variables allpaths, startnode and endnode.

allpaths = True
startnode = 0
endnode = 9


class MRBFSInit(MRJob):

    def mapper(self,_,line):

        x = line.replace("\n","").strip().split(" ")

        id = x[0]
        if int(x[0]) == startnode:
            dist = 0
            path = x[0]
        else:
            dist = inf
            path = ''

        adjacencylist = x[1:]

        if int(x[0]) == endnode and not allpaths:
            b = True
        else:
            b = False

        yield id,[id,dist,False,b,path,adjacencylist]

    def reducer(self,id,info):

        info = list(info)[0]

        s = ""
        for i in range(0,len(info[5])):
            s += (info[5][i] + " ")

        yield id, info[0] + "," + str(info[1]) + "," + str(info[2]) + "," + str(info[3]) + "," + info[4] + "," + s
