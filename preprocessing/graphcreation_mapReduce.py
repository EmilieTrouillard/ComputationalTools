#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 16:18:06 2018

@author: ubuntu
"""
import os
from mrjob.job import MRJob
from parserNoHash import parseJSON_FROMXML
from readGraph import readPickled
from indexcreation_mapReduce import TITLE_TO_ID_FILENAME, ID_TO_TITLE_FILENAME

HOME_DIR = '/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])
INPUT_FILE = HOME_DIR + '/sample/jsonNames.txt'
GRAPH_FILENAME = HOME_DIR + '/sample/graphfile_global_MergedRedirect_NoDuplicate'


# LOADING THE MAPPING ID TITLE
idtotitle = readPickled(TITLE_TO_ID_FILENAME)
print('import 1/2 done')
redirects = readPickled(ID_TO_TITLE_FILENAME)
print('import 2/2 done')


class aggregateGraph(MRJob):
        
    def mapper(self, _, line):

        INPUT_FILE = HOME_DIR + '/data/' + line
        
        parsed_dictionnaries = parseJSON_FROMXML(INPUT_FILE, idtotitle, redirects)

        yield 0, parsed_dictionnaries

    
    def reducer(self, _, values):

        pageClusters = list(values)
        graph = [[key] + links for cluster in pageClusters for key, links in cluster.items()]

        yield None, graph

mr_job = aggregateGraph(args=[INPUT_FILE])
with mr_job.make_runner() as runner:
    runner.run()
    with open(GRAPH_FILENAME,'w') as f1: 
    
        for _,value in mr_job.parse_output(runner.cat_output()):
            s = '\n'.join([' '.join(map(str, nodelist))  for nodelist in value])
            f1.write(s)
        f1.close()
