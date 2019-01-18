from flask import Flask,abort,render_template,request
from elasticsearch import Elasticsearch
import os
from pdf_indexing import create_index
import glob
import re
import requests


from numpy import array


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
    index_name = request.form.get('index')
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
    create_index(index_name)

    return render_template("search.html")


@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    indexes_list=[]
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

    url = "http://localhost:9200/_cat/indices?v"
    data = requests.get(url).content.decode('ascii')
    print("----------------------------------")

    lstr=re.split(" |\n", data)
    data=' '.join(lstr).split()
    matrix_list=[data[x:x + 10] for x in range(0, len(data), 10)]
    print(matrix_list)
    print("----------------------------------")

    print(res)
    print(res['hits']['total'])
    for index in es.indices.get('*'):
        indexes_list.append(index)
    return render_template('results.html', res=res,total_doc=upload.total_doc,indexes_list=indexes_list,matrix_list=matrix_list,matrix_length=len(matrix_list))


@app.route('/delete_index')
def delete_index():
    index_name = request.args.get('name')
    print("++++++++++++++++++++++++++++++++++++++++++++")
    print(index_name)
    es.indices.delete(index=index_name, ignore=[400, 404])


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='localhost', port=5000)