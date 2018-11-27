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

HOME_DIR = '/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])
INPUT_FILE = HOME_DIR + '/sample/jsonNames.txt'
TITLE_TO_ID_FILENAME = HOME_DIR + '/sample/title_to_id_mapNoRedirect'
ID_TO_TITLE_FILENAME = HOME_DIR + '/sample/id_to_title_mapNoRedirect'

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
