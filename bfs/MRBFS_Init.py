import mrjob
from mrjob.job import MRJob
from numpy import inf

allpaths = False
startnode = 0
endnode = 9


class MRBFSInit(MRJob):


    def mapper(self,_,list):

        x = list.replace("\n","").strip().split(" ")

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


        yield id,[id,dist,b,path,adjacencylist]

    def reducer(self,id,info):

        info = list(info)[0]

        s = ""
        for i in range(0,len(info[4])):
            s += (info[4][i] + " ")

        yield id, info[0] + "," + str(info[1]) + "," + str(info[2]) + "," + info[3] + "," + s
