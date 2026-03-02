from typing import List, Tuple
from sqlmodel import Session
from config.database import engine, init_db
from models.customer import Customer
from models.user import User
from models.g_user_facility import GUserFacility
from schemas.user import UsersXlsxRow
from utils.excel_reader import read_users_from_excel
from utils.password import hash_password
from utils.logger import get_logger

logger = get_logger(__name__)


class CustomerImportService:
    """顧客インポートサービス"""

    @staticmethod
    def load_from_excel(file_path: str) -> List[UsersXlsxRow]:
        """Excelファイルから顧客データを読み込む"""
        return read_users_from_excel(file_path)

    @staticmethod
    def check_diff(
        users: List[UsersXlsxRow],
    ) -> Tuple[List[UsersXlsxRow], List[UsersXlsxRow]]:
        """既存データとの差分をチェック"""
        init_db()
        with Session(engine) as session:
            existing_emails = {u.email for u in session.query(User).all()}

        new_users = []
        existing_users = []

        for user in users:
            if user.email in existing_emails:
                existing_users.append(user)
            else:
                new_users.append(user)

        return new_users, existing_users

    @staticmethod
    def import_customers(users: List[UsersXlsxRow]) -> int:
        """顧客データをデータベースに登録"""
        init_db()
        with Session(engine) as session:
            for user in users:
                user_obj = User(
                    name=user.name,
                    in_charge=user.in_charge,
                    company_name=user.company_name,
                    section_name=user.section_name,
                    email=user.email,
                    password=hash_password(user.password),
                )
                session.add(user_obj)
                session.flush()

                facility_id = f"{user.main_facility_number}_{user.sub_facility_number}"
                session.add(GUserFacility(user_id=user_obj.id, facility_id=facility_id))

                facility_id_zero = f"{user.main_facility_number}_0"
                session.add(
                    GUserFacility(user_id=user_obj.id, facility_id=facility_id_zero)
                )

            session.commit()

        logger.info(f"{len(users)}件のデータを登録しました")
        return len(users)
