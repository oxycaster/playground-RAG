import pandas as pd
import os
from openai import OpenAI
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import numpy as np
import time

def get_embedding(client, text, model="text-embedding-3-small"):
    """Get embedding for a text using OpenAI API"""
    if not text or pd.isna(text):
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

def combine_columns_text(row, columns):
    """Combine text from specified columns into a single string"""
    texts = []
    for col in columns:
        if col in row and not pd.isna(row[col]):
            texts.append(str(row[col]))
    return " ".join(texts)

def format_question_data(row, question_col, choice_cols, answer_col):
    """Format question data according to the specified template"""
    # Extract question text
    question_text = str(row[question_col]) if question_col in row and not pd.isna(row[question_col]) else ""

    # Extract choices text
    choices_text = []
    choice_labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

    for i, col in enumerate(choice_cols):
        if i < len(choice_labels) and col in row and not pd.isna(row[col]):
            choices_text.append(f"{choice_labels[i]}. {row[col]}")

    # Extract correct answer
    correct_answer = str(row[answer_col]) if answer_col in row and not pd.isna(row[answer_col]) else ""

    # Format according to template
    formatted_text = f"""<question>
{question_text}
</question>

<choices>
{chr(10).join(choices_text)}
</choices>

<correct_answer>
{correct_answer}
</correct_answer>"""

    return formatted_text

def main():
    # Path to the Excel file
    excel_file = "data/名称未設定.xlsx"

    # Check if file exists
    if not os.path.exists(excel_file):
        print(f"Error: File {excel_file} not found")
        return

    # Initialize OpenAI client
    # You need to set OPENAI_API_KEY environment variable or pass it directly
    try:
        client = OpenAI()
    except Exception as e:
        print(f"Error initializing OpenAI client: {e}")
        print("Make sure you have set the OPENAI_API_KEY environment variable")
        return

    # Initialize ChromaDB with persistence
    try:
        # Create chroma_db directory if it doesn't exist
        os.makedirs("chroma_db", exist_ok=True)

        # Initialize PersistentClient to store data in chroma_db directory
        chroma_client = chromadb.PersistentClient(path="chroma_db")
        print("Successfully initialized ChromaDB with persistence in 'chroma_db' directory")

        # Use OpenAI embeddings
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.environ.get("OPENAI_API_KEY"),
            model_name="text-embedding-3-small"
        )

        # Create or get collection
        collection = chroma_client.get_or_create_collection(
            name="excel_data_embeddings",
            embedding_function=openai_ef
        )
        print("Successfully connected to ChromaDB")
    except Exception as e:
        print(f"Error initializing ChromaDB: {e}")
        return

    # Read the Excel file
    try:
        df = pd.read_excel(excel_file)
        print(f"Successfully read Excel file with {len(df)} rows")

        # Get column names
        columns = df.columns.tolist()
        print(f"Columns: {columns}")

        # Identify required columns:
        # - Question: 36th column (index 35)
        # - Choices: 38th-44th columns (indices 37-43)
        # - Correct answer: 45th column (index 44)
        if len(columns) >= 45:
            question_col = columns[35]  # 36th column (index 35)
            choice_cols = [columns[37], columns[38], columns[39], columns[40], 
                          columns[41], columns[42], columns[43]]  # 38th-44th columns
            answer_col = columns[44]  # 45th column (index 44)
            print(f"Question column (36th column): {question_col}")
            print(f"Choice columns (38th-44th columns): {choice_cols}")
            print(f"Answer column (45th column): {answer_col}")
        else:
            print("Error: Excel file does not have at least 45 columns")
            print(f"File only has {len(columns)} columns")
            return

    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # Process each row and create embeddings
    print("Processing rows and creating embeddings...")
    for index, row in df.iterrows():
        try:
            # Format question data according to template
            formatted_text = format_question_data(row, question_col, choice_cols, answer_col)

            if not formatted_text:
                print(f"Skipping row {index+1} - no text data")
                continue

            # Get embedding
            embedding = get_embedding(client, formatted_text)

            if embedding:
                # Add to ChromaDB
                collection.add(
                    ids=[f"row_{index+1}"],
                    embeddings=[embedding],
                    metadatas=[{
                        "row_index": index + 1,
                        "source": excel_file,
                        "question": str(row[question_col]) if question_col in row and not pd.isna(row[question_col]) else "",
                        "correct_answer": str(row[answer_col]) if answer_col in row and not pd.isna(row[answer_col]) else ""
                    }],
                    documents=[formatted_text]
                )
                print(f"Processed row {index+1}")
            else:
                print(f"Skipping row {index+1} - failed to generate embedding")

        except Exception as e:
            print(f"Error processing row {index+1}: {e}")

    # Get collection count to verify
    count = collection.count()
    print(f"Successfully added {count} embeddings to ChromaDB")

if __name__ == "__main__":
    main()
