import mrjob
from mrjob.job import MRJob
from numpy import inf
import os
from mrjob.step import MRStep
#from mr3px.csvprotocol import CsvProtocol

class MRAPSP(MRJob):


    def steps(self):
        return [
            MRStep(mapper=self.mapper1, reducer=self.reducer1),
            MRStep(mapper=self.mapper2, combiner=self.reducer2, reducer=self.reducer2),
        ]

    def mapper1(self,_,line):


        s = line.split('"')

        i = s[1]
        j = s[3]

        m = s[4][2:]

        if m == 'Infinity':
            mij = inf
        else:
            mij = int(m)

        yield j,["M",i,mij]
        yield i,["N",j,mij]

    def reducer1(self,key,values):

        elementsFromM = []
        elementsFromN = []

        for value in values:
            if value[0]=="M":
                elementsFromM.append([value[1],value[2]])
            else:
                elementsFromN.append([value[1],value[2]])

        for eleM in elementsFromM:
            for eleN in elementsFromN:
                yield (eleM[0],eleN[0]), eleM[1]+eleN[1]

    def mapper2(self,key,value):

        yield key,value

    def reducer2(self,key,values):

        minDist = inf
        for value in values:
            if value < minDist:
                minDist = value

        yield key,minDist
