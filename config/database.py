from sqlmodel import create_engine, Session, SQLModel
from config.settings import settings

engine = create_engine(settings.DATABASE_URL, echo=True)


def init_db():
    """データベーステーブルを作成"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """データベースセッションを取得"""
    with Session(engine) as session:
        yield session
