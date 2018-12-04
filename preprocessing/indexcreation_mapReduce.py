#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 16:18:06 2018

@author: ubuntu
"""
from mrjob.job import MRJob
from parserNoHash import parseTITLES_FROMXML
import os
import pickle
import platform
from utilities import HOME_DIR
import argparse


INPUT_FILE = HOME_DIR + '/sample/jsonNames.txt'
TITLE_TO_ID_FILENAME = HOME_DIR + '/sample/title_to_id'
ID_TO_TITLE_FILENAME = HOME_DIR + '/sample/id_to_title'

class aggregateIndex(MRJob):

    def mapper(self, _, line):

        INPUT_FILE =  HOME_DIR + '/data/' + line

        parsed_titles = parseTITLES_FROMXML(INPUT_FILE)

        yield 0, list(parsed_titles)


    def reducer(self, _, values):
        counter = 0
        titleToIdMap = {}

        idToTitleMap = {}
        for setOfTitles in values:
            for title in setOfTitles:
                if title in titleToIdMap.keys():
                    continue
                titleToIdMap[title] = counter
                idToTitleMap[counter] = title
                counter += 1
                if counter % 1000 == 0:
                    print(counter)
        
        yield None, [titleToIdMap, idToTitleMap]

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_file", help="Name of file in which the name of the raw data files to consider are stored. DEFAULT '/sample/jsonNames.txt'", type=str)
parser.add_argument("-ti", "--title_to_id_filename", help="Name of the output title to id file. DEFAULT '/sample/title_to_id'", type=str)
parser.add_argument("-it", "--id_to_title_filename", help="Name of the output id to title file. DEFAULT '/sample/id_to_title'", type=str)
args = parser.parse_args()

if args.input_file != None:
    INPUT_FILE = HOME_DIR + args.input_file
if args.title_to_id_filename != None:
    TITLE_TO_ID_FILENAME = HOME_DIR + args.title_to_id_filename
if args.id_to_title_filename != None:
    ID_TO_TITLE_FILENAME = HOME_DIR + args.id_to_title_filename

mr_job = aggregateIndex(args=[INPUT_FILE])
with mr_job.make_runner() as runner:
    runner.run()
    with open(TITLE_TO_ID_FILENAME,'wb') as ft,  open(ID_TO_TITLE_FILENAME,'wb') as fi:

        for _,value in mr_job.parse_output(runner.cat_output()):
            print('Writing output files...')
            pickle.dump(value[0], ft)
            pickle.dump(value[1], fi)
        ft.close()
        fi.close()
