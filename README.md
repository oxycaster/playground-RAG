# Playground-RAG ベクトルストア作成・検索ツール

このツールは、Excelファイル（`data/名称未設定.xlsx`）を読み込み、AJ列（36列目）のテキストを処理し、OpenAIのAPIを使用して埋め込みベクトルを作成し、検索拡張生成（RAG）アプリケーション用にChromaDBに永続的に保存します。データは`chroma_db`ディレクトリに保存され、アプリケーションの再起動後も利用可能です。また、保存された埋め込みベクトルに対して類似検索を行い、入力されたテキストに最も関連性の高い上位10件の結果を取得することができます。

## 前提条件

- Python 3.13以上
- OpenAI APIキー

## インストール

1. このリポジトリをクローンする
2. 依存関係をインストールする：

```bash
uv pip install -r requirements.txt
```

## 設定

OpenAI APIキーを環境変数として設定します：

```bash
# Linux/macOSの場合
export OPENAI_API_KEY="your-api-key"

# Windowsの場合
set OPENAI_API_KEY=your-api-key
```

## 使用方法

### メインメニューの使用

メインスクリプトを実行すると、機能選択メニューが表示されます：

```bash
python main.py
```

メニューから以下の機能を選択できます：
1. ベクトルストアの作成
2. ベクトルストアの検索
q. 終了

### ベクトルストアの作成

メインメニューから「1」を選択するか、直接作成スクリプトを実行します：

```bash
python create_vector_store.py
```

これにより以下の処理が行われます：
1. Excelファイル `data/名称未設定.xlsx` を読み込む
2. 各行を処理し、AJ列（36列目）のテキストを取得する
3. OpenAIのAPIを使用して埋め込みベクトルを作成する
4. 埋め込みベクトルをChromaDBに永続的に保存する（`chroma_db`ディレクトリ内）

### ベクトルストアの検索

メインメニューから「2」を選択するか、直接検索スクリプトを実行します：

```bash
python search_vector_store.py "検索したいテキスト"
```

または、引数なしで実行すると対話的に検索テキストを入力できます：

```bash
python search_vector_store.py
```

これにより以下の処理が行われます：
1. 入力されたテキストをOpenAIのAPIを使用して埋め込みベクトルに変換する
2. ChromaDBに保存された埋め込みベクトルに対して類似検索を行う
3. 最も関連性の高い上位10件の結果を表示する

## ファイル構造

- `main.py`: アプリケーションのエントリーポイント
- `create_vector_store.py`: 埋め込みベクトルの作成と保存のための中核機能
- `search_vector_store.py`: 保存された埋め込みベクトルに対する検索機能
- `data/名称未設定.xlsx`: 処理対象の入力Excelファイル
- `requirements.txt`: Pythonの依存関係リスト
- `pyproject.toml`: プロジェクト設定
- `chroma_db/`: ChromaDBが埋め込みベクトルを永続的に保存するディレクトリ（自動生成）

## トラブルシューティング

問題が発生した場合：

1. OpenAI APIキーが正しく設定されていることを確認する
2. Excelファイルが存在し、期待される形式であることを確認する
3. すべての依存関係がuvを使用して正しくインストールされていることを確認する：
   ```bash
   uv sync
   ```
