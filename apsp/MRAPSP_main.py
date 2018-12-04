'''
IMPLEMENTATION OF ALL PAIRS SHORTEST PATH
INPUT:
* Graph Input file: the input_file should consist of lines of the form: <node_id> <neighbor_id1,neighbor_id2,...,neighbor_idk>
* (OPT) Output Dir: The user specifies where the output should be in output_dir. The program will create the directory output_dir/output,
    which should contain the output files after termination.
    During execution, the program will create the directory output_dir/MRAPSPTemp, where temporary files will be placed during execution.

RUN MRAPSP_main.py -h to learn more about arguments and options.

OUTPUT:
* The output has the form ["node_id1", "node_id2"] distance
---

'''
import mrjob
from mrjob.job import MRJob
from numpy import inf
from MRAPSP import MRAPSP
from math import log2
from math import ceil
import shutil
import os
import sys
import argparse

HOME_DIR = '/'.join(os.path.dirname(os.path.realpath(__file__)).replace('\\','/').split('/')[:-1])
OUTPUT_DIR_PARENT = HOME_DIR + '/sample'
OUTPUT_DIR = '/outputMRAPSP'
TEMP_DIR_NAME = "/MRAPSPTemp"
NODE_INFO_DIR_NAME = "/a"

working_dir = OUTPUT_DIR_PARENT + TEMP_DIR_NAME + NODE_INFO_DIR_NAME 


def initialization(input_file):

    with open(input_file) as f:

        F = f.readlines()

        D = [['Infinity' for i in range(0,len(F))] for j in range(0,len(F))]

        for i in range (0,len(F)):
            line = F[i]
            nodes = line.strip().split(" ")
            D[i][int(nodes[0])] = 0
            for node in nodes[1:]:
                D[i][int(node)] = 1

    write(D)
    return len(F)

def write(D):
    with open(working_dir + "0/input",'w') as f:
        for i in range (0,len(D)):
            for j in range(0,len(D)):
                f.write('["' + str(i) + '", "' + str(j) + '"]\t' + str(D[i][j]) + '\n')

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Graph input file")
    args = parser.parse_args()
    input_file = args.input_file

    if os.path.exists(working_dir[:-2]):
        shutil.rmtree(working_dir[:-2])
    os.makedirs(working_dir + "0")

    n = initialization(input_file)
    nIterations = ceil(log2(n-1))

    for i in range (0, nIterations):
        mr_job = MRAPSP(args=[working_dir + str(i)] + ['--output-dir=' + working_dir + str(i+1)])
        with mr_job.make_runner() as runner:
            runner.run()
            shutil.rmtree(working_dir + str(i-1),ignore_errors=True)

    mr_job = MRAPSP(args=[working_dir + str(nIterations)] + ['--output-dir=' + OUTPUT_DIR_PARENT + OUTPUT_DIR])
    with mr_job.make_runner() as runner:
        runner.run()
        shutil.rmtree(OUTPUT_DIR_PARENT + TEMP_DIR_NAME)

    print('All done! Go see {0} for the output'.format(OUTPUT_DIR_PARENT + OUTPUT_DIR))

