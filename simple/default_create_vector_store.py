import chromadb

chroma_client = chromadb.PersistentClient(path="chroma_db_default_embed")

collection = chroma_client.get_or_create_collection(
    name="hogehoge",
)

collection.add(
    ids=["id_1", "id_2"],
    metadatas=[{"hoge": "fuga"}, {"hoge": "piyo"}],
    documents=["これはテストの文書その１です", "これはテキスト２です"]
)
