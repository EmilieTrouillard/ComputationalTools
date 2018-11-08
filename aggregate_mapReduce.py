#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 16:18:06 2018

@author: ubuntu
"""
import mrjob
from mrjob.job import MRJob
from mrjob.step import MRStep
from parser import parseJSON_FROMXML
import pickle
from readGraph import readPickled

class aggregateDict(MRJob):
    # these are the defaults
    #INPUT_PROTOCOL = mrjob.protocol.RawValueProtocol
    #INTERNAL_PROTOCOL = mrjob.protocol.JSONProtocol
    #OUTPUT_PROTOCOL = mrjob.protocol.JSONProtocol
    def mapper(self, _, line):
        fileName = '/media/ubuntu/1TO/DTU/courses/ComputationalToolsForDataScience/ComputationalTools/parsed/' + line
        parsed_dictionnaries, _ = parseJSON_FROMXML(fileName)
        yield 0, parsed_dictionnaries
    
                    
    def reducer(self, key, values):
        D = {int(k):links for d in values for k,links in d.items()}
                
                
        #print(serialized)
        #outfile.close()
        yield (None, D)
    
    """def one_dict(self, _, D):
        print(D)
        yield list(D)
    
    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.one_dict)]"""
    
        
#if __name__ == '__main__':
#    aggregateDict.run()
#    #outfile = open('/media/ubuntu/1TO/DTU/courses/ComputationalToolsForDataScience/ComputationalTools/parsed/serializeSmall', 'wb')
#    #pickle.dump(out, outfile)
#    #outfile.close()

mr_job = aggregateDict(args=['jsonNames100.txt'])
with mr_job.make_runner() as runner:
    runner.run()
    for line in runner.stream_output():
        key, value = mr_job.parse_output_line(line)
        dictWithIntKeys = {int(k): links for k, links in value.items()}
        outfile = open('MapReduce100','wb')
        pickle.dump(dictWithIntKeys, outfile)
        outfile.close()
