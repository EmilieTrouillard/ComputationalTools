#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 16:18:06 2018

@author: ubuntu
"""

from mrjob.job import MRJob
from parserNoHash import parseTITLES_FROMXML
import pickle

fileName = '../data/jsonNames.txt'
#fileName = '../jsonNames1.txt'


class aggregateIndex(MRJob):

    def mapper(self, _, line):

        #print("line = " + line)
        fileName = '/media/ubuntu/1TO/DTU/courses/ComputationalToolsForDataScience/ComputationalTools/parsed/' + line
        #fileName = "C:/Users/Finn/Dropbox/02807/project/computationaltools/" + line

        parsed_titles = parseTITLES_FROMXML(fileName)

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

#print(fileName)
mr_job = aggregateIndex(args=[fileName])
with mr_job.make_runner() as runner:
    runner.run()
    with open('titletoidmapNoRedirect','wb') as ft,  open('idtotitlemapNoRedirect','wb') as fi:

        for _,value in mr_job.parse_output(runner.cat_output()):
            print('Writing output files...')
            pickle.dump(value[0], ft)
            pickle.dump(value[1], fi)
        ft.close()
        fi.close()
#            for title in value[1]:
#                f2.write(title + " " + str(value[1][title]))
#            for id in value[2]:
#                f3.write(id + " " + value[2][id])


            #for line in runner.util.to_lines(runner.cat_output()):
        #key, value = mr_job.parse_output(line)


        #outfile = open('graphfile','wb')
        #pickle.dump(value[0],outfile)
        #outfile.close()
        #outfile = open('titletoidmap','wb')
        #pickle.dump(value[1],outfile)
        #outfile.close()
        #outfile = open('idtotitlemap','wb')
        #pickle.dump(value[2],outfile)
        #dictWithIntKeys = {int(k): links for k, links in value.items()}
        #outfile = open('MapReduceAll','wb')
        #pickle.dump(dictWithIntKeys, outfile)
        #outfile.close()
