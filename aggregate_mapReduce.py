#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 16:18:06 2018

@author: ubuntu
"""

from mrjob.job import MRJob
from parser import parseJSON_FROMXML
import pickle

fileName = 'jsonNames.txt'

class aggregateDict(MRJob):
    
    def mapper(self, _, line):
        fileName = '/media/ubuntu/1TO/DTU/courses/ComputationalToolsForDataScience/ComputationalTools/parsed/' + line
        parsed_dictionnaries, _, _ = parseJSON_FROMXML(fileName)
        yield 0, parsed_dictionnaries
    
                    
    def reducer(self, key, values):
        D = {int(k):links for d in values for k,links in d.items()}
                
        yield (None, D)

mr_job = aggregateDict(args=[fileName])
with mr_job.make_runner() as runner:
    runner.run()
    for line in runner.util.to_lines(runner.cat_output()):
        key, value = mr_job.parse_output(line)
        dictWithIntKeys = {int(k): links for k, links in value.items()}
        outfile = open('MapReduceAll','wb')
        pickle.dump(dictWithIntKeys, outfile)
        outfile.close()
