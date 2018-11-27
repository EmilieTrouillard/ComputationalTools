#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 16:18:06 2018

@author: ubuntu
"""
import os
from mrjob.job import MRJob
from parserNoHash import parseREDIRECT_FROMXML
import pickle

HOME_DIR = '/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])
INPUT_FILE = HOME_DIR + '/sample/jsonNames.txt'
REDIRECT_DICT_FILENAME = HOME_DIR + '/sample/RedirectDict'

class aggregateIndex(MRJob):

    def mapper(self, _, line):

        INPUT_FILE = HOME_DIR + '/data/' + line

        parsed_titles = parseREDIRECT_FROMXML(INPUT_FILE)

        yield 0, parsed_titles


    def reducer(self, _, values):
        
        D = {k: link for d in values for k, link in d.items()}
        
        yield None, D
        
mr_job = aggregateIndex(args=[INPUT_FILE])
with mr_job.make_runner() as runner:
    runner.run()
    with open(REDIRECT_DICT_FILENAME,'wb') as f:

        for _,value in mr_job.parse_output(runner.cat_output()):
            print('Writing output file...')
            pickle.dump(value, f)
        f.close()
