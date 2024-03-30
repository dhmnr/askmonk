from llama_index.llms.mistralai import MistralAI
from llama_index.embeddings.mistralai import MistralAIEmbedding
from llama_index.core.query_engine import RetrieverQueryEngine

from llama_index.core import (StorageContext, 
                              ServiceContext, 
                              VectorStoreIndex, 
                              SimpleDirectoryReader,
                              ChatPromptTemplate)

from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch

from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Settings

import pymongo 
from pymongo.mongo_client import MongoClient

def _set_settings_():

    api_key=''

    llm = MistralAI(api_key=api_key, model="mistral-large-latest")
    embed_model = MistralAIEmbedding(model_name="mistral-embed", api_key=api_key)

    Settings.llm = llm
    Settings.embed_model = embed_model
    Settings.node_parser = SentenceSplitter(chunk_size=128, chunk_overlap=20)
    Settings.num_output = 8192
    Settings.context_window = 32000


def get_mongo_client():
    uri = ""

    client = MongoClient(uri)
    try:
        client.admin.command('ping')
        #print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    return client

def create_vector_data(store, path):
    
    uber_docs = SimpleDirectoryReader(input_dir=path).load_data()

    storage_context = StorageContext.from_defaults(vector_store=store)

    index = VectorStoreIndex.from_documents(
            uber_docs, storage_context = storage_context
    )
    
    return index, store


def retrieve_(store, query=None):

    ret_index = VectorStoreIndex.from_vector_store(vector_store = store)
    query_engine = ret_index.as_query_engine(similarity_top_k = 8)

    resp2 = query_engine.query(query)

    return resp2


def test():
    client = get_mongo_client()

    store = MongoDBAtlasVectorSearch(client, 
                                     index_name='mistr', 
                                     db_name='attn_db', 
                                     collection_name='vec')
    return retrieve_(store, "How do I make PacMan get best score in BigMaze problem?")

if __name__ == '__main__':
    _set_settings_()
    print(test())
