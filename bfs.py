'''
Implementation of bfs for our data structure:
{Node:[Neighbors]}
'''
from numpy import inf as infinite

def getMinDistFromNeighbors(neighbors, visited):
    # Get the minimum distance from the neighbors nodes
    minDist = infinite
    for neighbor in neighbors:
        if visited[neighbor] < minDist:
            minDist = visited[neighbor]
    return minDist

def bfs(graph,start,end,dist=0,visited=None):
    # Initialization
    # Visited format: {Node:dist to end}
    if visited is None:
        visited = {start: infinite}

    # If start is not in the graph, return infinite
    if start not in graph:
        visited[start] = infinite
        return visited[start]

    neighbors = graph[start]
    # STOP criterion
    # No neighbors
    if len(neighbors) == 0:
        visited[start] = infinite

    # RECURRENCE:
    # Either the dist + 1 if the end is in the neighbors
    if end in neighbors:
        return dist + 1
    # Or 1 + min of the dist of the neighbors
    # Let's first get the distances of the neighbors
    else:
        for neighbor in neighbors:
            # If not visited, call the bfs on the neighbor
            if neighbor not in visited:
                visited[neighbor] = bfs(graph, neighbor, end, dist + 1, visited) # This will update the visited dict used to get the min distance
        visited[start] = getMinDistFromNeighbors(neighbors, visited)


    return visited[start]

if __name__ == '__main__':

    testGraph = {
        1: [2],
        2: [3,4],
        4: [5]
    }
    print(bfs(testGraph,1,6))
