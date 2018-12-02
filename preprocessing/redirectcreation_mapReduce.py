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
from utilities import HOME_DIR
import argparse

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

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_file", help="Name of file in which the name of the raw data files to consider are stored. DEFAULT '/sample/jsonNames.txt'", type=str)
parser.add_argument("-o", "--output_file", help="Name of the output redirect file. DEFAULT '/sample/RedirectDict'", type=str)
args = parser.parse_args()

if args.input_file != None:
    INPUT_FILE = HOME_DIR + args.input_file
if args.output_file != None:
    REDIRECT_DICT_FILENAME = HOME_DIR + args.output_file
        
mr_job = aggregateIndex(args=[INPUT_FILE])
with mr_job.make_runner() as runner:
    runner.run()
    with open(REDIRECT_DICT_FILENAME,'wb') as f:

        for _,value in mr_job.parse_output(runner.cat_output()):
            print('Writing output file...')
            pickle.dump(value, f)
        f.close()
