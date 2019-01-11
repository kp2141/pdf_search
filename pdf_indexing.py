from elasticsearch import Elasticsearch
import tika
tika.TikaClientOnly = True
from tika import parser
from dateutil.parser import parse
import glob
import os

es_client = Elasticsearch(['http://127.0.0.1:9200'])
drop_index = es_client.indices.create(index='pdf-index', ignore=400)
create_index = es_client.indices.delete(index='pdf-index', ignore=[400, 404])

def pdf_parser(file_path):
    parsed = parser.from_file(file_path, 'http://localhost:9998/tika')
    print(parsed['metadata'])
    print("--------------------------------------")
    file_name=os.path.basename(file_path)
    doc = {
            'content':parsed['content'],
           #'title': parsed['metadata']['title'],
           # 'author': parsed['metadata']['Author']
            'title':file_name,
       }
    res = es_client.index(index='pdf-index', doc_type= 'docs',body=doc)
    print(res)

names_pdf = glob.glob(r"C:\Users\BISAG\PycharmProjects\pdf_search\pdf_files\*.*")
final_list = []
count=0
for i in names_pdf:
    pdf_parser(i)
    count+=1
    print(count)


