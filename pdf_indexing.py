from elasticsearch import Elasticsearch
import tika
tika.TikaClientOnly = True
from tika import parser
import glob
import os
import time
es_client = Elasticsearch(['http://127.0.0.1:9200'])


def pdf_parser(file_path, index_name):
    parsed = parser.from_file(file_path, 'http://localhost:9998/tika')
    print(parsed)
    print("--------------------------------------")
    file_name=os.path.basename(file_path)
    creation_date=time.ctime(os.path.getctime(file_path))
    if 'Author' in parsed['metadata'] and parsed['metadata']['Author']!="":
        doc = {
                'content':parsed['content'],
                'creation-date':creation_date,
               'author': parsed['metadata']['Author'],
                'title':file_name,
           }
    else:
        doc = {
            'content': parsed['content'],
            'creation-date': creation_date,
            'author': 'Unknown',
            'title': file_name,
        }

    res = es_client.index(index=index_name, doc_type= 'docs',body=doc)
    print(res)

def create_index(index_name):
    create_index = es_client.indices.create(index=index_name, ignore=400)
    #delete_index = es_client.indices.delete(index=index_name, ignore=[400, 404])
    names_pdf = glob.glob(r"C:\Users\BISAG\PycharmProjects\pdf_search\uploaded_files\*.*")
    count=0
    for i in names_pdf:
        pdf_parser(i,index_name)
        count+=1
        print(count)
