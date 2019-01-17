from flask import Flask,abort,render_template,request
from elasticsearch import Elasticsearch
import os
from pdf_indexing import create_index
import glob


app = Flask(__name__)
es = Elasticsearch('http://127.0.0.1', port=9200)

APP_ROOT=os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def home():
    return render_template('search.html')

@app.route("/upload",methods=['POST'])
def upload():
    target=os.path.join(APP_ROOT,'uploaded_files')
    print(target)
    files = glob.glob(r"C:\Users\BISAG\PycharmProjects\pdf_search\uploaded_files\*.*")
    for f in files:
        os.remove(f)

    if not os.path.isdir(target):
        os.mkdir(target)
    total_document = 0
    for file in request.files.getlist("file"):
        print(file)
        filename=file.filename
        destination="/".join([target,filename])
        print(destination)
        file.save(destination)
        total_document+=1
    upload.total_doc=total_document
    create_index()
    return render_template("search.html")


@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]

    res = es.search(
        index="pdf-index",
        body={
            "query": {
               "match_phrase" : {
                    'content': search_term,
                }
            }
        }
    )

    print(res)
    print(res['hits']['total'])

    return render_template('results.html', res=res,total_doc=upload.total_doc)

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='localhost', port=5000)