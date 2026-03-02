from typing import Optional
from sqlmodel import Field, SQLModel


class GUserFacility(SQLModel, table=True):
    """g_user_facilityテーブル用のモデル"""

    __tablename__ = "g_user_facility"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    facility_id: str = Field(index=True)
