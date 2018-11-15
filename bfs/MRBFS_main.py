import mrjob
from mrjob.job import MRJob
from MRBFS import MRBFS
from MRBFS_Init import MRBFSInit
from numpy import inf
import sys
import shutil
import os

input_file = "../data/input.txt"
nodeinfo_dir = "../data/temp"
#output_dir = "../data/temp2"

def write(job,runner):

    with open(nodeinfo_file,'w') as f:

        for key,value in job.parse_output(runner.cat_output()):

            f.write(value)

            f.write("\n")


if __name__ == "__main__":

    #singleEndnode = (len(sys.argv) > 1)
    #startnode = int(sys.argv[1])
    #endnode = int(sys.argv[2])
    if os.path.exists(nodeinfo_dir):
        shutil.rmtree(nodeinfo_dir)
    if not os.path.exists(nodeinfo_dir):
        os.makedirs(nodeinfo_dir)
#    if os.path.exists(output_dir):
#        shutil.rmtree(output_dir)
#    if not os.path.exists(output_dir):
#        os.makedirs(output_dir)

    mr_job = MRBFSInit(args=["../data/input.txt"] + ['--output-dir=' + nodeinfo_dir])
    with mr_job.make_runner() as runner:
        runner.run()


    nFoundNodes = 1

    while True:

        mr_job = MRBFS(args=[nodeinfo_dir] +['--output-dir=' + nodeinfo_dir])
        with mr_job.make_runner() as runner:
            runner.run()

            #shutil.rmtree(nodeinfo_dir,ignore_errors=True)
            #os.rename(output_dir,nodeinfo_dir)
            #shutil.rmtree(output_dir,ignore_errors=True)
            if not runner.counters()[0] or len(runner.counters()[0]) == 2:
                break
            c = runner.counters()[0]["nFoundNodes"][""]
            if c > nFoundNodes:
                nFoundNodes = c
            else:
                break
