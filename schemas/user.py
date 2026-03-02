from pydantic import BaseModel, Field, field_validator


class UsersXlsxRow(BaseModel):
    """Excelファイルから読み込むユーザー情報"""

    name: str = Field(validation_alias="名前")
    in_charge: str = Field(validation_alias="担当営業所")
    company_name: str = Field(validation_alias="会社名")
    section_name: str = Field(validation_alias="部署名")
    email: str = Field(validation_alias="メールアドレス")
    password: str = Field(validation_alias="パスワード")
    notifiable: str = Field(default=1, validation_alias="メール通知")
    main_facility_number: str = Field(validation_alias="紐づけ受検施設番号")
    sub_facility_number: str = Field(validation_alias="紐づけ受検施設サブ番号")

    @field_validator(
        "password", "main_facility_number", "sub_facility_number", mode="before"
    )
    def cast_to_str(cls, v):
        return str(v) if v is not None else ""

    @field_validator("section_name", mode="before")
    def cast_section_name_to_str(cls, v):
        return str(v) if v is not None else ""
