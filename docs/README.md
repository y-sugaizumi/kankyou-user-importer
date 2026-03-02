# 顧客データインポートツール

ExcelファイルからMySQLデータベースに顧客データをインポートするツールです。

## 機能

- Excelファイル（.xlsx）からの顧客データ読み込み
- 既存データとの差分チェック
- パスワードのbcryptハッシュ化（Laravel互換）
- GUI（Webブラウザ）とCUIの両対応
- SQLite（開発環境）とMySQL（本番環境）の切り替え

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. 環境設定

開発環境（デフォルト）:
```bash
# 自動的にSQLiteを使用
python app.py
```

本番環境:
```bash
export ENV=production
export DATABASE_URL="mysql+mysqlconnector://user:password@host/dbname"
python app.py
```

## 使い方

### GUI版（推奨）

```bash
python app.py
```

ブラウザで http://localhost:8550 を開き、ファイルを選択してインポート。

### CUI版

```bash
python ui/cli.py
```

対話形式でファイルパスを入力してインポート。

## プロジェクト構成

```
20250110/
├── app.py                    # GUI起動
├── main.py                   # 既存CLI
├── requirements.txt          # 依存関係
├── services/                 # ビジネスロジック
│   └── customer_import.py
├── ui/                       # プレゼンテーション層
│   ├── cli.py               # CUI
│   └── flet_app.py          # GUI
├── models/                   # ORMモデル
│   └── customer.py
├── schemas/                  # バリデーション
│   └── user.py
├── config/                   # 設定
│   ├── database.py
│   └── settings.py
├── utils/                    # ユーティリティ
│   ├── excel_reader.py
│   ├── logger.py
│   └── password.py
└── docs/                     # ドキュメント
    ├── README.md
    └── architecture.md
```

## ライセンス

使用しているライブラリ:
- Flet (Apache 2.0) - GUI
- SQLModel (MIT) - ORM
- Pydantic (MIT) - バリデーション
- bcrypt (Apache 2.0) - パスワードハッシュ化

## ビルド

EXEファイルへのビルド方法は [docs/build.md](build.md) を参照してください。
