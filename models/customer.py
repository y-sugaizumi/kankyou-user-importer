from typing import Optional
from sqlmodel import Field, SQLModel


class Customer(SQLModel, table=True):
    """データベーステーブル用のモデル"""
    __tablename__ = "customers"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    address: str = Field(index=True)
    login_name: str = Field(index=True)
    department: str
    name: str = Field(index=True)
    email: str = Field(index=True)
    password: str
