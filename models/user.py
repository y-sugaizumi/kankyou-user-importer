from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """usersテーブル用のモデル"""
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    in_charge: str
    company_name: str = Field(index=True)
    section_name: str
    email: str = Field(index=True)
    password: str
    notifiable: int = Field(default=1)
    individual_batch_flag: int = Field(default=0)
    role_id: int = Field(default=100)
