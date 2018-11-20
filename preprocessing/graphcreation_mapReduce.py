#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 16:18:06 2018

@author: ubuntu
"""

from mrjob.job import MRJob
from parserNoHash import parseJSON_FROMXML
from readGraph import readPickled

fileName = '../data/jsonNames.txt'
#fileName = '../jsonNames1.txt'
idtotitle = readPickled('titletoidmapNoRedirect')
print('import 1/2 done')
redirects = readPickled('RedirectDict')
print('import 2/2 done')


class aggregateGraph(MRJob):
        
    def mapper(self, _, line):

        fileName = '/media/ubuntu/1TO/DTU/courses/ComputationalToolsForDataScience/ComputationalTools/parsed/' + line
        #fileName = "C:/Users/Finn/Dropbox/02807/project/computationaltools/" + line

        
        parsed_dictionnaries = parseJSON_FROMXML(fileName, idtotitle, redirects)

        yield 0, parsed_dictionnaries

    
    def reducer(self, _, values):


        pageClusters = list(values)
        graph = [[key] + links for cluster in pageClusters for key, links in cluster.items()]


        yield None, graph

mr_job = aggregateGraph(args=[fileName])
with mr_job.make_runner() as runner:
    runner.run()
    with open('graphfile_global_MergedRedirect_NoDuplicate','w') as f1: 
    
        for _,value in mr_job.parse_output(runner.cat_output()):
            s = '\n'.join([' '.join(map(str, nodelist))  for nodelist in value])
            f1.write(s)
        f1.close()
