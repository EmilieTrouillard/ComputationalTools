'''
IMPLEMENTATION OF SHORTEST PATH THROUGH MAP REDUCE
INPUT:
* Graph input file: It should consist of lines of the form: <node_id> <neighbor_id1,neighbor_id2,...,neighbor_idk>
* Output dir: The user specifies where the output should be in OUTPUT_DIR_PARENT. The program will create the directory OUTPUT_DIR_PARENT/output,
    which should contain the output files after termination.
    During execution, the program will create the directory OUTPUT_DIR_PARENT/MRBFSTemp, where temporary files will be placed during execution.
OUTPUT:
* The output has the form: "id" "id,distance,hasSent,isEndnode,path,adjacencylist"
---
The startnode and the endnode should be set in MRBFS_Init.py, and the user can specify whether he/she wants all paths or only the path to the endnode.
Then run this script to use the algorithm.


isEndnode is only True for the endnode, and hasSent is used just for the algorithm and can be ignored in the output.
'''
import mrjob
from mrjob.job import MRJob
from MRBFS import MRBFS
from MRBFS_Init import MRBFSInit, changeStartNode, changeEndNode, changeAllPaths
from numpy import inf
import sys
import shutil
import os
import argparse


HOME_DIR = '/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])
OUTPUT_DIR_PARENT = HOME_DIR + '/sample'
OUTPUT_DIR = '/outputMRBFS'
TEMP_DIR_NAME = "/MRBFSTemp"
NODE_INFO_DIR_NAME = "/a"

nodeinfo_dir = OUTPUT_DIR_PARENT + TEMP_DIR_NAME + NODE_INFO_DIR_NAME


if __name__ == "__main__":

    ## HANDLE ARGUMENTS
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Graph input file")
    parser.add_argument("-s", "--startnode", help="ID of the starting node", type=int)
    parser.add_argument("-e", "--endnode", help="ID of the end node", type=int)
    parser.add_argument("-a", "--allpaths", help="Specify if it should find path to all nodes. (0 for NO, 1 for YES) DEFAULT:YES", type=int, choices=[0, 1])
    parser.add_argument("-o", "--output_dir", help="Directory to store output in")
    parser.add_argument("-op", "--output_dir_parent", help="Parent directory to store output in")
    args = parser.parse_args()

    input_file = args.input_file

    if args.startnode:
        changeStartNode(args.startnode)
    if args.endnode:
        changeEndNode(args.endnode)
    if (args.allpaths == 0 or args.allpaths == 1):
        changeAllPaths(bool(args.allpaths))
    if args.output_dir_parent:
        OUTPUT_DIR_PARENT = args.output_dir_parent
    if args.output_dir:
        OUTPUT_DIR = args.output_dir

    if os.path.exists(nodeinfo_dir[:-2]):
        try:
            shutil.rmtree(nodeinfo_dir[:-2])
        except OSError as e:
            print("Please close directory " + OUTPUT_DIR_PARENT + "/")
            sys.exit(0)
    try:
        os.makedirs(nodeinfo_dir)
    except PermissionError as e:
        print("Please close directory " + OUTPUT_DIR_PARENT + "/")
        sys.exit(0)

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


    mr_job = MRBFS(args=[nodeinfo_dir + str(i)] + ['--output-dir=' + OUTPUT_DIR_PARENT + OUTPUT_DIR])
    with mr_job.make_runner() as runner:
        runner.run()
        shutil.rmtree(OUTPUT_DIR_PARENT + TEMP_DIR_NAME)
