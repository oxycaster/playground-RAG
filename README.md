# Playground-RAG ベクトルストア作成ツール

このツールは、Excelファイル（`data/名称未設定.xlsx`）を読み込み、AJ列（36列目）のテキストを処理し、OpenAIのAPIを使用して埋め込みベクトルを作成し、検索拡張生成（RAG）アプリケーション用にChromaDBに保存します。

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

メインスクリプトを実行します：

```bash
python main.py
```

これにより以下の処理が行われます：
1. Excelファイル `data/名称未設定.xlsx` を読み込む
2. 各行を処理し、AJ列（36列目）のテキストを取得する
3. OpenAIのAPIを使用して埋め込みベクトルを作成する
4. 埋め込みベクトルをChromaDBに保存する

## ファイル構造

- `main.py`: アプリケーションのエントリーポイント
- `create_vector_store.py`: 埋め込みベクトルの作成と保存のための中核機能
- `data/名称未設定.xlsx`: 処理対象の入力Excelファイル
- `requirements.txt`: Pythonの依存関係リスト
- `pyproject.toml`: プロジェクト設定

## トラブルシューティング

問題が発生した場合：

1. OpenAI APIキーが正しく設定されていることを確認する
2. Excelファイルが存在し、期待される形式であることを確認する
3. すべての依存関係がuvを使用して正しくインストールされていることを確認する：
   ```bash
   uv pip install -r requirements.txt
   ```

## ライセンス

[MITライセンス](LICENSE)
