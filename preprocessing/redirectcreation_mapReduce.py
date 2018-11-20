#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 16:18:06 2018

@author: ubuntu
"""

from mrjob.job import MRJob
from parserNoHash import parseREDIRECT_FROMXML
import pickle

fileName = '../data/jsonNames.txt'
#fileName = '../jsonNames1.txt'


class aggregateIndex(MRJob):

    def mapper(self, _, line):

        #print("line = " + line)
        fileName = '/media/ubuntu/1TO/DTU/courses/ComputationalToolsForDataScience/ComputationalTools/parsed/' + line
        #fileName = "C:/Users/Finn/Dropbox/02807/project/computationaltools/" + line

        parsed_titles = parseREDIRECT_FROMXML(fileName)

        yield 0, parsed_titles


    def reducer(self, _, values):
        
        D = {k: link for d in values for k, link in d.items()}
        
        yield None, D
        
#print(fileName)
mr_job = aggregateIndex(args=[fileName])
with mr_job.make_runner() as runner:
    runner.run()
    with open('RedirectDict','wb') as f:

        for _,value in mr_job.parse_output(runner.cat_output()):
            print('Writing output file...')
            pickle.dump(value, f)
        f.close()
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
