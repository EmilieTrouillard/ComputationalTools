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

    def printVerifiedNode(self, tx, pageTitle):
        for record in tx.run("MATCH (b: Page {title: {pageTitle}}) RETURN b", pageTitle=pageTitle):
            return record

    def verifyNodes(self, start, end):
        verified = True
        print('Verifying the nodes', start, end)
        with self.driver.session() as session:
            try:
                startNode = session.read_transaction(self.printVerifiedNode, start)
                endNode = session.read_transaction(self.printVerifiedNode, end)
                if (startNode == None or endNode == None):
                    verified = False
            except TypeError as e:
                verified = False
        return verified

    def executeShortestPathQuery(self, tx, start, end):
        '''
        Returns only one shortest path!
        '''
        for record in tx.run(
            "MATCH (b: Page {title: {start}}), (e: Page {title: {end}}), p = shortestPath((b)-[:LINKS_TO*]->(e)) RETURN b,e,p", start=start, end=end):
            return record['p'] # 'p' is the key to access the path object

    def getShortestPath(self, start, end):
        shortestPath, validNodes = [], True
        with self.driver.session() as session:
            path = session.read_transaction(self.executeShortestPathQuery, start, end)
        try:
            for node in path.nodes:
                shortestPath.append(node)
        except AttributeError:
            print('No path found')
        return shortestPath


class GraphInterpreter:
    '''
    Class to make the interface between the graph objects
    and the rest of the app.
    '''

    def __init__(self):
        # DB can't handle these characters in the title of the pages
        self.charmap = {
            '"': "''",
            ";": ",",
            "_": " "
        }

    def remapCharactersTitle(self, title):
        for badChar, goodChar in self.charmap.items():
            title = title.replace(badChar, goodChar)
        return title

    def interpretNode(self, node):
        return node.__getitem__('title')

    def interpretPath(self, path):
        if len(path) == 0:
            return None
        outputPath = []
        for node in path:
            outputPath.append(self.interpretNode(node))
        return outputPath

## TEST 

if __name__ == '__main__':
    worker = GraphWorker()
    worker.getShortestPath('Apple', 'Denmark')