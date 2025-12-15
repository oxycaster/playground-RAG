import chromadb

chroma_client = chromadb.PersistentClient(path="chroma_db_default_embed")

collection = chroma_client.get_collection(
    name="hogehoge",
)

results = collection.query(query_texts=["テスト"], n_results=10)

print(results)
