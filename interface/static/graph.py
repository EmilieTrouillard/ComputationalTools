'''
File that handles the wikipedia's graph.
Most notably, access the graph db for querying the shortest path
'''
from neo4j.v1 import GraphDatabase


class GraphWorker:
    '''
    Interface to work with the graph database.
    See https://neo4j.com/docs/api/python-driver/current/_modules/neo4j/v1/types/graph.html#Path
    '''

    def __init__(self):
        self.DB_URI = "bolt://localhost:7687"
        self.AUTH_CREDENTIAL = "neo4j"
        self.AUTH_PASSWORD = "WikipediaIsAwesome!"

        self.driver = GraphDatabase.driver(self.DB_URI, auth=(self.AUTH_CREDENTIAL, self.AUTH_PASSWORD))


    def executeShortestPathQuery(self, tx, start, end):
        for record in tx.run(
            "MATCH (b: Page {pageId: {start}}), (e: Page {pageId: {end}}), p = shortestPath((b)-[:LINKS_TO*]->(e)) "
            "RETURN p", start=int(start), end=int(end)):
            return record['p'] # 'p' is the key to access the path object

    def getShortestPath(self, start, end):
        shortestPath = []
        with self.driver.session() as session:
            path = session.read_transaction(self.executeShortestPathQuery, start, end)
        for node in path.nodes:
            shortestPath.append(node)
        return shortestPath


class GraphInterpreter:
    '''
    Class to make the interface between the graph objects
    and the rest of the app.
    '''

    def __init__(self):
        # TO REDO ONCE WE HAVE THE ACTUAL MAPPING
        # READ FROM SERIALIZED ?
        self.mapper = {
            'page1': 1,
            'page2': 2,
            'page3': 3,
            'page4': 4,
            'page5': 5,
            'page6': 6,
        }

    def translateNameId(self, page):
        return self.mapper[page]

    def translateIdName(self, id):
        # TO OPTIMIZE
        for page, pageId in self.mapper.items():
            if pageId == id:
                return page

    def interpretNode(self, node):
        return self.translateIdName(node.__getitem__('pageId'))

    def interpretPath(self, path):
        outputPath = []
        for node in path:
            outputPath.append(self.interpretNode(node))
        return '->'.join(outputPath)

## TEST 

if __name__ == '__main__':
    worker = GraphWorker()
    worker.getShortestPath(0, 5)