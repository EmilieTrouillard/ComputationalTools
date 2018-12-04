from flask import Flask
from flask import request
from flask import render_template

from static import graph

app = Flask(__name__)

@app.route('/')
def index():
    firstPage, secondPage, validPages, path = request.args.get('firstpage'), request.args.get('secondpage'), True, None

    # QUICK SECURITY
    if firstPage != None:
        if len(firstPage) > 500:
            firstPage = None
    if secondPage != None:
        if len(secondPage) > 500:
            secondPage = None


    # GETTING THE SHORTEST PATH:
    if firstPage != None and secondPage != None:
        graphWorker, graphInterpreter = graph.GraphWorker(), graph.GraphInterpreter()
        firstPage, secondPage = graphInterpreter.remapCharactersTitle(firstPage), graphInterpreter.remapCharactersTitle(secondPage)
        dbPath = graphWorker.getShortestPath(firstPage, secondPage)

        # If no path is found, verify the validity of the nodes
        if len(dbPath) == 0:
            validPages = graphWorker.verifyNodes(firstPage, secondPage)

        # Interpret the path
        path = graphInterpreter.interpretPath(dbPath)

    if firstPage == None:
        firstPage = ''
    if secondPage == None:
        secondPage = ''
    return render_template('interface.html', firstpage=firstPage, secondpage=secondPage, path=path, validpages=validPages)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
