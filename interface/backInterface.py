from flask import Flask
from flask import request
from flask import render_template

from static import graph

app = Flask(__name__)

@app.route('/')
def index():
    firstPage, secondPage = request.args.get('firstpage'), request.args.get('secondpage');

    path = ''
    # GETTING THE SHORTEST PATH:
    if firstPage != None and secondPage != None:
        graphWorker, graphInterpreter = graph.GraphWorker(), graph.GraphInterpreter()
        dbPath = graphWorker.getShortestPath(firstPage, secondPage)
        path = graphInterpreter.interpretPath(dbPath)
    if firstPage == None:
        firstPage = ''
    if secondPage == None:
        secondPage = ''
    return render_template('interface.html', firstpage=firstPage, secondpage=secondPage, path=path)
