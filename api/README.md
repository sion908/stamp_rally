# api を記述する

aiomysql
https://aiomysql.readthedocs.io/en/stable/connection.html

## poetry 系

依存関係の解決用  
requirements.txt みたいなやつ

### 依存関係

最初の依存関係のインストール

```shell
poetry install
```

個別のライブラリのインストール、アンインストール

```shell
# dependenciesに追加
poetry add jinja2
# 本番環境以外の場合はgroup指定
poetry add --group (dev|test|linter) jinja2

# dependenciesから削除
poetry remove jinja2
```

### migration ファイルの作成

詳しくは[README](src/database/migrations/README.md)を確認

```shell
./run.sh createmmigration {description}
```

### FastAPI の起動

1. コンテナの起動

```shell
docker-compose -f api/docker/docker-compose.yaml up
```

2. fastapi の起動

```shell
npm run fastapi
```

で fastapi を起動可能です。
fastapi の swagger を確認するには、`http://localhost/docs`にアクセスしてください。

### test 関連

## ディレクトリ構成

### １層目

```python
api/
├ docker/            # docker系
├ docs/              # ドキュメント
├ (python_modules/)  # ライブラリ格納場所
├ (.venv/)           # 仮想環境ライブラリ格納場所
├ src/               # ソースコード全般
├ tests/             # テストコード
├ run.sh             # 全体的なコマンドを確認するためのシェルスクリプト, ./run.shで内容確認
└ pyproject.toml     # poetryの設定ファイル
```

### ２層目

#### docker ディレクトリ

```python
api/
└ docker/
  ├ mysql/               # mysqlの永続用フォルダ、初期設定のファイルも含む
  ├ .env                 # docker-compose用の設定ファイル、プロジェクト名やポートの指定、.env.sampleのコピー
  ├ app.env              # yamltoenvでの自動生成、appの環境変数
  ├ docker-compose.yaml  # dockerの本体
  └ Doeckerfile          # appのdokcerファイル
```

#### src ディレクトリ

```python
api/
└ src/
  ├ assets/          # 画像データなど,static?
  ├ crud/            # CRUD操作に関する処理
  ├ database/        # DBの設定系
  ├ models/          # DBモデルの定義
  ├ routers/         # ルーティング後のエンドポイント
  ├ schemas/         # APIのI/O定義
  ├ services/        # CRUD以外の処理
  ├ dependencies.py  # 依存性注入 認証とか
  └ main.py          # エンドポイントの設定
```

#### test ディレクトリ

```python
api/
└ tests/
  ├ integration/    # 総合テスト
  ├ unit/           # 単体テスト
  ├ conftest.py     # テストの設定
  └ dependencies.py # 依存性の上書き
```

### 3 層目

#### database ディレクトリ

```python
api/
└ src/
  └ database/
    ├ migrations/      # migrationのための設定ファイル
    │ ├ versions/      # 生成されたmigrationファイルの置き場
    │ ├ env.py         # migrationファイル生成時の前処理等
    │ ├ README.md      # alembic系の設定など
    │ └ script.py.mako # migrationファイル生成の雛形
    ├ alembic.ini      # migrationのための設定ファイル
    ├ base_class.py    # modelのBaseクラス定義
    └ db.py            # db接続の定義
```

## VScode におけるライブラリの依存関係の解消のやり方

下記を`.vscode/settings.json`に追加することで自動で補完が行われるようになる
追跡済み

```json
{
    "python.autoComplete.extraPaths": [
        "api/python_modules/local/lib/python3.10/site-packages"
    ],
    "python.analysis.extraPaths": [
        "api/python_modules/local/lib/python3.10/site-packages"
    ]
}
```
