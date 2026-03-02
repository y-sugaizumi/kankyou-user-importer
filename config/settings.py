import sys
import os
from pathlib import Path
from typing import Literal
from dotenv import load_dotenv


class Settings:
    # EXE実行時のパスを取得
    if getattr(sys, 'frozen', False):
        # PyInstallerやflet buildでビルドされた場合
        BASE_DIR = Path(sys.executable).parent
    else:
        # 通常の実行
        BASE_DIR = Path(__file__).parent.parent
    
    # .envファイルを読み込み（EXEと同じディレクトリから）
    env_path = BASE_DIR / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    
    ENV: Literal["development", "production"] = os.getenv("ENV", "development")
    
    # 開発環境ではSQLite、本番環境ではMySQL
    DATABASE_URL: str = (
        f"sqlite:///{BASE_DIR / 'database.db'}"
        if ENV == "development" 
        else os.getenv("DATABASE_URL", "mysql+mysqlconnector://username:password@localhost/dbname")
    )


settings = Settings()
