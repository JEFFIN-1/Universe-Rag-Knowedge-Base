from elasticsearch import Elasticsearch
import json


def get_es_client():
    # connect to Elasticsearch
    pass


def create_index(es, index_name, dims):
    # create index if it doesn't exist
    pass


def load_chunks(path):
    # load chunks.json
    pass


def upload_chunks(es, index_name, chunks):
    # upload all chunks
    pass


def count_documents(es, index_name):
    # return document count
    pass


def delete_index(es, index_name):
    # delete index if needed
    pass