import os

import chromadb
from chromadb.utils import embedding_functions

chroma_client = chromadb.PersistentClient(path="chroma_db_openai_embed")

# chromadbが色々なラッパーを作ってくれている
# see: https://docs.trychroma.com/docs/embeddings/embedding-functions
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.environ.get("OPENAI_API_KEY"),
    model_name="text-embedding-3-small"
)

collection = chroma_client.get_or_create_collection(
    name="piyopiyo",
    embedding_function=openai_ef  # 上で作ったEmbedding Functionを設定するだけ
)

collection.add(
    ids=["id_1", "id_2"],
    metadatas=[{"hoge": "fuga"}, {"hoge": "piyo"}],
    documents=["これはテストの文書その１です", "これはテキスト２です"]
)
