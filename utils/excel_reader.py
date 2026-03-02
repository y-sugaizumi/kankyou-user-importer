import numpy as np
import pandas as pd
from typing import List
from schemas.user import UsersXlsxRow
from utils.logger import get_logger
from exceptions import ExcelFormatError
from validators import validate_excel_file

logger = get_logger(__name__)


def read_users_from_excel(file_path: str) -> List[UsersXlsxRow]:
    """Excelファイルからユーザー情報を読み込む"""
    validate_excel_file(file_path)

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        raise ExcelFormatError(f"Excelファイルの読み込みに失敗しました: {str(e)}")

    df = df.replace({np.nan: None})

    users = []
    for index, row in df.iterrows():
        try:
            user = UsersXlsxRow.model_validate(row.to_dict())
            users.append(user)
        except Exception as e:
            logger.exception(f"Excelの行のパースエラー: {str(e)}")
            raise ExcelFormatError(
                f"{index + 2}行目: 必要な列（名前、担当営業所、会社名、部署名、メールアドレス、パスワード）が見つかりません"
            )

    return users
