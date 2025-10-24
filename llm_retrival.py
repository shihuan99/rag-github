import os

import httpx
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding

from silicon_llm import SiliconFlowLLM

embed_model =  OpenAIEmbedding(api_key=os.environ['API_KEY'], api_base=os.environ['BASE_URL'], model_name='BAAI/bge-m3', http_client=httpx.Client(verify=False))

def build_query_engine(documents):
    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
    return index.as_query_engine(llm=SiliconFlowLLM())