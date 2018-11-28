import mrjob
from mrjob.job import MRJob
from MRBFS import MRBFS
from MRBFS_Init import MRBFSInit
from numpy import inf
import sys
import shutil
import os


## input_file should consist of lines of the form: <node_id> <neighbor_id1,neighbor_id2,...,neighbor_idk>
## The user specifies where the output should be in output_dir. The program will create the directory output_dir/output,
## which should contain the output files after termination.
## During execution, the program will create the directory output_dir/MRBFSTemp, where temporary files will be placed during execution.

## The startnode and the endnode should be set in MRBFS_Init.py, and the user can specify whether he/she wants all paths or only the path to the endnode.
## Then run this script to use the algorithm.

## The output has the form: "id" "id,distance,hasSent,isEndnode,path,adjacencylist"
## isEndnode is only True for the endnode, and hasSent is used just for the algorithm and can be ignored in the output.



#input_file = "D:/02807Project_data/graphfile_global_MergedRedirect_NoDuplicate"
#input_file = "../data/input.txt"

output_dir = "D:/02807Project_data/MRBFS"

nodeinfo_dir = output_dir + "/MRBFSTemp/a"


if __name__ == "__main__":


    if os.path.exists(nodeinfo_dir[:-2]):
        try:
            shutil.rmtree(nodeinfo_dir[:-2])
        except OSError as e:
            print("Please close directory " + output_dir + "/")
            sys.exit(0)
    try:
        os.makedirs(nodeinfo_dir)
    except PermissionError as e:
        print("Please close directory " + output_dir + "/")
        sys.exit(0)

    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    mr_job = MRBFSInit(args=[input_file] + ['--output-dir=' + nodeinfo_dir + "0"])

    with mr_job.make_runner() as runner:
        runner.run()


    nFoundNodes = 1
    i = 0
    while True:
        i += 1
        mr_job = MRBFS(args=[nodeinfo_dir + str(i-1)] + ['--output-dir=' + nodeinfo_dir + str(i)])
        with mr_job.make_runner() as runner:
            runner.run()

            shutil.rmtree(nodeinfo_dir + str(i-1),ignore_errors=True)

            if not runner.counters()[0] or len(runner.counters()[0]) == 3:
                break
            c = runner.counters()[0]["nFoundNodes"][""]
            if c > nFoundNodes:
                nFoundNodes = c
            else:
                break


    mr_job = MRBFS(args=[nodeinfo_dir + str(i)] + ['--output-dir=' + output_dir + "/output"])
    with mr_job.make_runner() as runner:
        runner.run()
        shutil.rmtree(output_dir + "/MRBFSTemp")
