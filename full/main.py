def main():
    print("Playground-RAG - ベクトルストア作成・検索ツール")
    print("------------------------------------------")

    # Import required modules
    try:
        import create_vector_store
        import search_vector_store
    except ImportError as e:
        print(f"Error importing modules: {e}")
        print("Make sure all dependencies are installed by running:")
        print("uv pip install -r requirements.txt")
        return

    # Display menu
    print("\n機能を選択してください:")
    print("1. ベクトルストアの作成")
    print("2. ベクトルストアの検索")
    print("q. 終了")

    choice = input("\n選択 (1/2/q): ").strip().lower()

    if choice == '1':
        # Run the vector store creation process
        try:
            print("\nベクトルストア作成プロセスを開始します...")
            create_vector_store.main()
            print("ベクトルストア作成プロセスが完了しました。")
        except Exception as e:
            print(f"ベクトルストア作成中にエラーが発生しました: {e}")

    elif choice == '2':
        # Run the vector store search process
        try:
            print("\nベクトルストア検索プロセスを開始します...")
            query = input("検索するテキストを入力してください: ")
            if query.strip():
                results = search_vector_store.search_vector_store(query)
                search_vector_store.display_results(results)
            else:
                print("検索テキストが入力されていません。")
        except Exception as e:
            print(f"ベクトルストア検索中にエラーが発生しました: {e}")

    elif choice == 'q':
        print("プログラムを終了します。")

    else:
        print("無効な選択です。1、2、またはqを入力してください。")


if __name__ == "__main__":
    main()
