#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 16:18:06 2018

@author: ubuntu
"""

from mrjob.job import MRJob
from parserNoHash import parseJSON_FROMXML
import pickle

#fileName = '../data/jsonNames.txt'
fileName = '../jsonNames1.txt'

class aggregateGraph(MRJob):

    def mapper(self, _, line):

        #print("line = " + line)
        fileName = '/media/ubuntu/1TO/DTU/courses/ComputationalToolsForDataScience/ComputationalTools/parsed/' + line
        #fileName = "C:/Users/Finn/Dropbox/02807/project/computationaltools/" + line


        parsed_dictionnaries, _, _ = parseJSON_FROMXML(fileName)

        yield 0, parsed_dictionnaries


    def reducer(self, _, values):

        #values: generator, where each element is a dictionary {nodetitle: list of neighbortitles}
        #nodes: list of dictionaries {nodetitle: list of neighbortitles}

        nodes = list(values)

        titleToIdMap = {}
        idToTitleTap = {}
        counter = 0
        for dictOfPages in nodes:
            for pageTitle in dictOfPages.keys():
                titleToIdMap[pageTitle] = counter
                idToTitleTap[counter] = pageTitle
                counter += 1

        graph = [[i] for i in range(counter)] # First number is the id. The remaining numbers are the neighbors.

        for dictOfPages in nodes:
            for pageTitle, links in dictOfPages.items():
                for neighborTitle in links:
                    #print(str(pagetitle) + ": " + str(neighbortitle))
                    #print(neighbortitle)
                    if neighborTitle in titleToIdMap:
                        graph[titleToIdMap[pageTitle]].append(titleToIdMap[neighborTitle])


        yield None, [graph, titleToIdMap, idToTitleTap]

#print(fileName)
mr_job = aggregateGraph(args=[fileName])
with mr_job.make_runner() as runner:
    runner.run()
    with open('graphfile','w') as f1, open('titletoidmap','wb') as f2, open('idtotitlemap','wb') as f3:

        for _,value in mr_job.parse_output(runner.cat_output()):
            s = ' '.join([' '.join(map(str, nodelist)) + '\n' for nodelist in value[0]])
            f1.write(s)
#                for i in range(0,len(nodelist)):
#                    f1.write(str(nodelist[i]) + " ")
#                f1.write("\n")
            pickle.dump(value[1], f2)
            pickle.dump(value[2], f3)
#            for title in value[1]:
#                f2.write(title + " " + str(value[1][title]))
#            for id in value[2]:
#                f3.write(id + " " + value[2][id])


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
