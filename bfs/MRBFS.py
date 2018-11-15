import mrjob
from mrjob.job import MRJob
from numpy import inf
import os

class MRBFS(MRJob):

    # list format: id,dist,isEndnode,path,adjacencylist
    def mapper(self,_,list):

        s = list.split('"')[3].strip().split(',')

        id = s[0]
        if s[1] == "inf":
            dist = inf
        else:
            dist = int(s[1])

        if s[2] == "True":
            isEndnode = True
        else:
            isEndnode = False
        path = s[3]
        adjacencylist = s[4].split(" ")

        yield id, [id,dist,isEndnode,path,adjacencylist]

        for n in adjacencylist:
            if n != "":
                yield n,[dist+1,path]

    def reducer(self,id,distandpath):

        dmin = inf
        N = None
        path = None

        for d in distandpath:
            if len(d) > 2:
                N = d
            elif d[0] < dmin:
                dmin = d[0]
                path = d[1] + " " + id
        if dmin < N[1]:
            N[1] = dmin
            N[3] = path
            if N[2]:
                self.increment_counter("endnode","",1)
                print(path)

        if N[1] < inf:
            self.increment_counter("nFoundNodes","",1)

        s = ""
        for i in range(0,len(N[4])):
            s += (N[4][i] + " ")

        yield id, N[0] + "," + str(N[1]) + "," + str(N[2]) + "," + N[3] + "," + s
