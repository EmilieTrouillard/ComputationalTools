#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 16:18:06 2018

@author: ubuntu
"""

from mrjob.job import MRJob
from parser2 import parseJSON_FROMXML
import pickle

fileName = 'jsonNames2.txt'

class aggregateGraph(MRJob):

    def mapper(self, _, line):

        print("line = " + line)
        #fileName = '/media/ubuntu/1TO/DTU/courses/ComputationalToolsForDataScience/ComputationalTools/parsed/' + line
        fileName = "C:/Users/Finn/Dropbox/02807/project/computationaltools/" + line


        parsed_dictionnaries, _, _ = parseJSON_FROMXML(fileName)

        yield 0, parsed_dictionnaries


    def reducer(self, _, values):

        #values: generator, where each element is a dictionary {nodetitle: list of neighbortitles}
        #nodes: list of dictionaries {nodetitle: list of neighbortitles}

        nodes = list(values)

        titletoidmap = {}
        idtotitlemap = {}
        counter = 0
        for i in range(0,len(nodes)):
            for pagetitle in nodes[i]:
                titletoidmap[pagetitle] = counter
                idtotitlemap[counter] = pagetitle
                counter += 1

        graph = [[i] for i in range(0,counter)] # First number is the id. The remaining numbers are the neighbors.

        for i in range(0,len(nodes)):
            for pagetitle in nodes[i]:
                for neighbortitle in nodes[i][pagetitle]:
                    #print(str(pagetitle) + ": " + str(neighbortitle))
                    #print(neighbortitle)
                    if neighbortitle in titletoidmap:
                        graph[titletoidmap[pagetitle]].append(titletoidmap[neighbortitle])


        yield None, [graph, titletoidmap, idtotitlemap]

#print(fileName)
mr_job = aggregateGraph(args=[fileName])
with mr_job.make_runner() as runner:
    runner.run()
    with open('graphfile','w') as f1, open('titletoidmap','w') as f2, open('idtotitlemap','w') as f3:

        for _,value in mr_job.parse_output(runner.cat_output()):
            for nodelist in value[0]:
                for i in range(0,len(nodelist)):
                    f1.write(str(nodelist[i]) + " ")
                f1.write("\n")
            for title in value[1]:
                f2.write(title + " " + str(value[1][title]))
            for id in value[2]:
                f3.write(id + " " + value[2][id])


            #for line in runner.util.to_lines(runner.cat_output()):
        #key, value = mr_job.parse_output(line)


        #outfile = open('graphfile','wb')
        #pickle.dump(value[0],outfile)
        #outfile.close()
        #outfile = open('titletoidmap','wb')
        #pickle.dump(value[1],outfile)
        #outfile.close()
        #outfile = open('idtotitlemap','wb')
        #pickle.dump(value[2],outfile)
        #dictWithIntKeys = {int(k): links for k, links in value.items()}
        #outfile = open('MapReduceAll','wb')
        #pickle.dump(dictWithIntKeys, outfile)
        #outfile.close()
