# ビルド手順

## EXEファイルへのビルド

Fletの`flet build`コマンドを使用してワンファイルのEXEを作成できます。

### 前提条件

```bash
pip install flet
```

### ビルドコマンド

**Windows用EXE:**
```bash
flet build windows
```

**オプション:**
- `--onefile` - 単一のEXEファイルにパッケージ化
- `--name "顧客データインポートツール"` - アプリ名を指定
- `--icon icon.ico` - アイコンを指定

**完全なコマンド例:**
```bash
flet build windows --onefile --name "CustomerImport"
```

### ビルド成果物

ビルド後、以下に生成されます:
```
build/windows/CustomerImport.exe
```

### 注意事項

1. **データベースファイル**
   - SQLiteの`database.db`は実行ファイルと同じディレクトリに配置
   - または環境変数で別の場所を指定

2. **Excelファイル**
   - ユーザーが選択するため、同梱不要

3. **設定ファイル**
   - `.env`ファイルは実行ファイルと同じディレクトリに配置

### 配布パッケージ構成

```
CustomerImport/
├── CustomerImport.exe    # ビルドされた実行ファイル
├── database.db           # SQLiteデータベース（初回起動時に自動生成）
└── .env                  # 環境設定（オプション）
```

### 設定ファイルの扱い

**開発環境（デフォルト）:**
- 設定ファイル不要
- EXEと同じディレクトリに`database.db`が自動生成される

**本番環境（MySQL使用）:**

EXEと同じディレクトリに`.env`ファイルを配置:

```env
ENV=production
DATABASE_URL=mysql+mysqlconnector://user:password@host/dbname
```

`.env`ファイルは自動的に読み込まれます。

## 代替方法: PyInstaller

Fletのビルドがうまくいかない場合、PyInstallerも使用可能:

```bash
pip install pyinstaller

pyinstaller --onefile --windowed \
  --name CustomerImport \
  --add-data "config:config" \
  --add-data "models:models" \
  --add-data "schemas:schemas" \
  --add-data "services:services" \
  --add-data "ui:ui" \
  --add-data "utils:utils" \
  app.py
```

## トラブルシューティング

### ビルドエラーが出る場合

1. 依存関係を明示的に指定:
```bash
pip freeze > requirements.txt
```

2. 仮想環境をクリーンに:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Fletを最新版に:
```bash
pip install --upgrade flet
```

### 実行時エラーが出る場合

- ログを確認: `--verbose` オプションでビルド
- パスの問題: 相対パスではなく絶対パスを使用
- DLLエラー: Visual C++ Redistributableをインストール

## サイズ削減

EXEファイルサイズを削減するには:

1. 不要な依存関係を削除
2. `--optimize` オプションを使用
3. UPXで圧縮（オプション）

```bash
flet build windows --onefile --optimize
```

## クロスプラットフォーム

**macOS用:**
```bash
flet build macos
```

**Linux用:**
```bash
flet build linux
```

**Web版（ブラウザで動作）:**
```bash
flet build web
```
