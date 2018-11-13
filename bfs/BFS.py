import mrjob
from mrjob.job import MRJob

class MRBFS(MRJob):

    # list format: id,dist,False,adjacencylist[]]
    def mapper(self,_,list):

        str = list.split(" ")
        id = int(str[0])
        dist = int(str[1])
        found = list[2]

        adjacencylist = [int(j) for j in str[3:]]

        yield id, [id,dist,found,adjacencylist]

        for n in adjacencylist:
            yield n,dist+1

    def reducer(self,id,dist):

        dist = list(dist)

        dmin = 1000000000000
        N = None
        found = False

        for d in dist:
            if(type(d)==list):
                N = d
                d = N[1]
            if d < dmin:
                dmin = d
        if dmin < N[1]:
            found = True
            N[1] = dmin
        N[2] = found

        yield id, N
