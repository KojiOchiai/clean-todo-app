# clean-todo-app
todo app to learn clean architecture

## セットアップ

1. リポジトリをクローン
```bash
git clone git@github.com:KojiOchiai/clean-todo-app.git
cd clean-todo-app
```

2. 依存関係をインストール
```bash
uv sync
```

3. フロントエンドの依存関係をインストール（Web UIを使用する場合）
```bash
cd app/frontend
npm install
cd ../..
```

## 起動方法

### Web UIで起動
```bash
uv run python main.py --storage file --ui web
```

アプリケーション起動後、ブラウザで http://localhost:8000/static/ にアクセス

### CLI版で起動
```bash
uv run python main.py --storage file --ui cli
```

### ストレージオプション
- `--storage file`: JSONファイル（デフォルト）
- `--storage sqlite`: SQLiteデータベース
- `--storage memory`: メモリ内ストレージ（テスト用）
