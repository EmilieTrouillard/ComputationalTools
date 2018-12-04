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
import argparse
from utilities import HOME_DIR
import copy

INPUT_FILE = HOME_DIR + '/sample/jsonNames.txt'
DATA_DIR = '/data/'
GRAPH_FILENAME = HOME_DIR + '/sample/graphfile'


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_file", help="Name of file in which the name of the raw data files to consider are stored. DEFAULT '/sample/jsonNames.txt'", type=str)
parser.add_argument("-o", "--output_file", help="Name of the output graph file. DEFAULT '/sample/graphfile'", type=str)
parser.add_argument("-d", "--data_dir", help="Name of the directory in which the raw data is stored (json Files). DEFAULT '/data/'", type=str)
parser.add_argument("-ti", "--title_to_id_filename", help="Name of the title to id file.", type=str)
parser.add_argument("-it", "--id_to_title_filename", help="Name of the id to title file.", type=str)
args = parser.parse_args()

from indexcreation_mapReduce import TITLE_TO_ID_FILENAME, ID_TO_TITLE_FILENAME
TITLE_TO_ID_FILENAME_L = TITLE_TO_ID_FILENAME
ID_TO_TITLE_FILENAME_L = ID_TO_TITLE_FILENAME

if args.input_file != None:
    INPUT_FILE = HOME_DIR + args.input_file
if args.output_file != None:
    GRAPH_FILENAME = HOME_DIR + args.output_file
if args.data_dir != None:
    DATA_DIR = HOME_DIR + args.data_dir
if args.title_to_id_filename != None:
    TITLE_TO_ID_FILENAME_L = HOME_DIR + args.title_to_id_filename
if args.id_to_title_filename != None:
    ID_TO_TITLE_FILENAME_L =  HOME_DIR + args.id_to_title_filename

# LOADING THE MAPPING ID TITLE
idtotitle = readPickled(TITLE_TO_ID_FILENAME)
print('import 1/2 done')
redirects = readPickled(ID_TO_TITLE_FILENAME)
print('import 2/2 done')


class aggregateGraph(MRJob):
        
    def mapper(self, _, line):

        INPUT_FILE = HOME_DIR + DATA_DIR + line
        
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
