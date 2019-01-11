from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
import pdf_indexing
app = Flask(__name__)
es = Elasticsearch('http://127.0.0.1', port=9200)
import datetime
@app.route('/')
def home():
    return render_template('search.html')

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
    return render_template('results.html', res=res )

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='localhost', port=5000)