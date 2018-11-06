#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 16:18:06 2018

@author: ubuntu
"""

from mrjob.job import MRJob
from parser import parseJSON_FROMXML

class aggregateDict(MRJob):
    def mapper(self, _, line):
        fileName = '/media/ubuntu/1TO/DTU/courses/ComputationalToolsForDataScience/ComputationalTools/parsed/' + line
        parsed_dictionnaries, _ = parseJSON_FROMXML(fileName)
        yield 0, parsed_dictionnaries
    
                    
    def reducer(self, key, values):
        D = dict()
        for d in values:
            for page_id, links in d.items():
                D[page_id] = links
        yield(key, D)

if __name__ == '__main__':
    aggregateDict.run()

