from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__)

@app.route('/')
def index():
    firstPage, secondPage = request.args.get('firstpage'), request.args.get('secondpage');
    if firstPage == None:
        firstPage = ''
    if secondPage == None:
        secondPage = ''
    return render_template('interface.html', firstpage=firstPage, secondpage=secondPage, path='test')
