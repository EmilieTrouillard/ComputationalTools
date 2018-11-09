#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 13:54:40 2018

@author: ubuntu
"""

from mrjob.job import MRJob
from parser import parseJSON_FROMXML
import pickle

fileName = 'jsonNames.txt'

class aggregateDict(MRJob):
    
    def mapper(self, _, line):
        fileName = '/media/ubuntu/1TO/DTU/courses/ComputationalToolsForDataScience/ComputationalTools/parsed/' + line
        _ , redirect_links, hash_titles = parseJSON_FROMXML(fileName)
        yield 0, (redirect_links, hash_titles)
    
                    
    def reducer(self, key, values):
        DLinks = {int(k):link for d in values for k,link in d[0].items()}
        DTitles = {int(k):link for d in values for k,link in d[1].items()}
                
        yield (None, (DLinks, DTitles))

mr_job = aggregateDict(args=[fileName])
with mr_job.make_runner() as runner:
    runner.run()
    for line in runner.stream_output():
        key, value = mr_job.parse_output_line(line)
        linkDictWithIntKeys = {int(k): link for k, link in value[0].items()}
        titleDictWithIntKeys = {int(k): link for k, link in value[1].items()}
        outfilelink = open('MapReduceRedirectLinks','wb')
        pickle.dump(linkDictWithIntKeys, outfilelink)
        outfilelink.close()
        outfiletitle = open('MapReduceRedirectTitles','wb')
        pickle.dump(titleDictWithIntKeys, outfiletitle)
        outfiletitle.close()
