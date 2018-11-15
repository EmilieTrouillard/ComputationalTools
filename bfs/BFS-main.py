import mrjob
from mrjob.job import MRJob
from MRBFS import MRBFS
from shutil import copyfile
import sys

input_file = "temp/input.txt"
nodeinfo_file = "temp/nodeinfo.txt"

def getnodes(job,runner):

    nodes = []
    for line in runner.stream_output():

        key,value = job.parse_output_line(line)

        node = [value[0]]
        node.append(value[1])
        for n in value[2:]:
            node.append(n)

        nodes.append(node)

    return nodes

def write(nodes):

    go_on = False

    with open(nodeinfo_file,'w') as f:
        for node in nodes:
            f.write(str(node[0]) + " ")
            f.write(str(node[1]) + " ")

            found = node[2]

            if found:
                go_on = True
            f.write("False")

            adjacencylist = node[3]
            if len(adjacencylist) > 0:
                f.write(" ")
            for i in range(0,len(adjacencylist)):
                n = adjacencylist[i]
                f.write(str(n))
                if i < len(adjacencylist)-1:
                    f.write(" ")
            f.write("\n")

    return go_on


def initialize_nodeinfo(startnode):
    with open(input_file,'r') as f1, open(nodeinfo_file,'w') as f2:
        for line in f1.readlines():
            line = line.replace("\n", "")
            x = line.split(" ")
            f2.write(x[0] + " ")
            if int(x[0]) == startnode:
                f2.write(str(0))
            else:
                f2.write(str(1000000000000))
            f2.write(" False")

            if len(x) > 1:
                for i in range (1,len(x)):
                    f2.write(" ")
                    f2.write(x[i])
            f2.write("\n")

#copyfile(input_file,nodeinfo_file)


if __name__ == "__main__":

    startnode = int(sys.argv[1])

    initialize_nodeinfo(startnode)


    go_on = True
    while go_on:
        print("Iteration:")
        mr_job = MRBFS(args=[nodeinfo_file])
        with mr_job.make_runner() as runner:
            runner.run()
            nodes = getnodes(mr_job,runner)
            go_on = write(nodes)