import os
import argparse
from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions
import time

def get_embedding(client, text, model="text-embedding-3-small"):
    """Get embedding for a text using OpenAI API"""
    if not text or not text.strip():
        return None

    # Convert to string if not already
    if not isinstance(text, str):
        text = str(text)

    # Retry mechanism for API calls
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.embeddings.create(
                input=text,
                model=model
            )
            return response.data[0].embedding
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Error getting embedding, retrying in {wait_time}s: {e}")
                time.sleep(wait_time)
            else:
                print(f"Failed to get embedding after {max_retries} attempts: {e}")
                return None

def search_vector_store(query_text, n_results=10):
    """
    Search the vector store for similar documents to the query text
    
    Args:
        query_text (str): The text to search for
        n_results (int): Number of results to return (default: 10)
        
    Returns:
        list: List of search results
    """
    # Initialize OpenAI client
    try:
        client = OpenAI()
    except Exception as e:
        print(f"Error initializing OpenAI client: {e}")
        print("Make sure you have set the OPENAI_API_KEY environment variable")
        return []

    # Initialize ChromaDB with persistence
    try:
        # Check if chroma_db directory exists
        if not os.path.exists("chroma_db"):
            print("Error: Vector database not found. Please run create_vector_store.py first.")
            return []

        # Initialize PersistentClient to access data in chroma_db directory
        chroma_client = chromadb.PersistentClient(path="chroma_db")
        print("Successfully connected to ChromaDB")

        # Use OpenAI embeddings
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.environ.get("OPENAI_API_KEY"),
            model_name="text-embedding-3-small"
        )

        # Get collection
        try:
            collection = chroma_client.get_collection(
                name="excel_data_embeddings",
                embedding_function=openai_ef
            )
            print(f"Successfully accessed collection with {collection.count()} documents")
        except Exception as e:
            print(f"Error accessing collection: {e}")
            print("Make sure you have run create_vector_store.py first to create the collection")
            return []

    except Exception as e:
        print(f"Error initializing ChromaDB: {e}")
        return []

    # Get embedding for query text
    query_embedding = get_embedding(client, query_text)
    if not query_embedding:
        print("Error: Failed to generate embedding for query text")
        return []

    # Query the collection
    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        print(f"Found {len(results['documents'][0])} matching documents")
        return results
    except Exception as e:
        print(f"Error querying collection: {e}")
        return []

def display_results(results):
    """Display search results in a readable format"""
    if not results or not results.get('documents') or not results['documents'][0]:
        print("No results found")
        return

    documents = results['documents'][0]
    metadatas = results['metadatas'][0]
    distances = results['distances'][0]

    print("\n===== Search Results =====")
    for i, (doc, meta, dist) in enumerate(zip(documents, metadatas, distances)):
        print(f"\n--- Result {i+1} (Similarity: {1-dist:.4f}) ---")
        print(f"Row: {meta.get('row_index', 'N/A')}")
        print(f"Source: {meta.get('source', 'N/A')}")
        
        # Print the document text (truncate if too long)
        max_length = 200
        if len(doc) > max_length:
            print(f"Text: {doc[:max_length]}...")
        else:
            print(f"Text: {doc}")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Search the vector store for similar documents')
    parser.add_argument('query', nargs='?', help='The text to search for')
    args = parser.parse_args()

    # Get query text from command line or prompt user
    query_text = args.query
    if not query_text:
        query_text = input("Enter text to search for: ")

    if not query_text.strip():
        print("Error: No query text provided")
        return

    # Search the vector store
    results = search_vector_store(query_text)
    
    # Display results
    display_results(results)

if __name__ == "__main__":
    main()