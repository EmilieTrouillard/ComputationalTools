import mrjob
from mrjob.job import MRJob
from numpy import inf
from MRAPSP import MRAPSP
from math import log2
from math import ceil
import shutil
import os
import sys


## input_file should consist of lines of the form: <node_id> <neighbor_id1,neighbor_id2,...,neighbor_idk>
## The user specifies where the output should be in output_dir. The program will create the directory output_dir/output,
## which should contain the output files after termination.
## During execution, the program will create the directory output_dir/MRAPSPTemp, where temporary files will be placed during execution.
## The output has the form ["node_id1", "node_id2"] distance


## After setting the output_dir, the user can run the program with 1 argument, which is the path of the input file.


output_dir = "D:/02807Project_data/MRAPSP"

working_dir = output_dir + "/MRAPSPTemp/a"


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

    if os.path.exists(working_dir[:-2]):
        shutil.rmtree(working_dir[:-2])
    os.makedirs(working_dir + "0")

    input_file = sys.argv[1]

    n = initialization(input_file)
    nIterations = ceil(log2(n-1))

    for i in range (0,nIterations):

        mr_job = MRAPSP(args=[working_dir + str(i)] + ['--output-dir=' + working_dir + str(i+1)])
        with mr_job.make_runner() as runner:
            runner.run()
            shutil.rmtree(working_dir + str(i-1),ignore_errors=True)

    mr_job = MRAPSP(args=[working_dir + str(nIterations)] + ['--output-dir=' + output_dir + "/output"])
    with mr_job.make_runner() as runner:
        runner.run()
        shutil.rmtree(output_dir + "/MRAPSPTemp")
