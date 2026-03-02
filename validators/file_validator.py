from pathlib import Path
from exceptions import ExcelFormatError
from utils.logger import get_logger

logger = get_logger(__name__)


def validate_file_exists(file_path: str) -> Path:
    """ファイルの存在を検証"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")
    if not path.is_file():
        raise ValueError(f"指定されたパスはファイルではありません: {file_path}")
    logger.info(f"ファイル検証成功: {file_path}")
    return path


def validate_excel_file(file_path: str) -> Path:
    """Excelファイルの存在と拡張子を検証"""
    path = validate_file_exists(file_path)
    if path.suffix.lower() not in [".xlsx", ".xls"]:
        raise ExcelFormatError(f"Excelファイル(.xlsx, .xls)を指定してください: {file_path}")
    logger.info(f"Excelファイル検証成功: {path.name}")
    return path
