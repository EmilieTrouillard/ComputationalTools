import mrjob
from mrjob.job import MRJob
from numpy import inf

class MRBFS(MRJob):

    # list format: id,dist,hasSent,isEndnode,path,adjacencylist
    def mapper(self,_,line):


        s = line.split('"')[3].strip().split(',')

        id = s[0]

        if s[1] == "inf":
            dist = inf
        else:
            dist = int(s[1])

        if s[2] == "True":
            hasSent = True
        else:
            hasSent = False

        if s[3] == "True":
            isEndnode = True
        else:
            isEndnode = False

        path = s[4]
        adjacencylist = s[5].split(" ")



        if not hasSent and dist < inf:
            for n in adjacencylist:
                if n != "":
                    yield n,[dist+1,path]
            hasSent = True


        yield id, [id,dist,hasSent,isEndnode,path,adjacencylist]


    def reducer(self,id,distandpath):

        dmin = inf
        N = None
        path = None

        for d in distandpath:
            if len(d) > 2:
                N = d
                self.increment_counter("Nodes","",1)
            elif d[0] < dmin:
                dmin = d[0]
                path = d[1] + " " + id
        if dmin < N[1]:
            N[1] = dmin
            N[4] = path
            if N[3]:
                self.increment_counter("endnode","",1)
                print(path)

        if N[1] < inf:
            self.increment_counter("nFoundNodes","",1)

        s = ""
        for i in range(0,len(N[5])):
            s += (N[5][i] + " ")


        yield id, N[0] + "," + str(N[1]) + "," + str(N[2]) + "," + str(N[3]) + "," + N[4] + "," + s
