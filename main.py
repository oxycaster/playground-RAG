def main():
    print("Playground-RAG - Vector Store Creation Tool")
    print("------------------------------------------")

    # Import the create_vector_store module
    try:
        import create_vector_store

        # Run the vector store creation process
        print("Starting vector store creation process...")
        create_vector_store.main()
        print("Vector store creation process completed.")
    except ImportError as e:
        print(f"Error importing create_vector_store module: {e}")
        print("Make sure all dependencies are installed by running:")
        print("pip install -r requirements.txt")
    except Exception as e:
        print(f"Error during vector store creation: {e}")


if __name__ == "__main__":
    main()
