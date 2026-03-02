from sqlmodel import Session
from config.database import engine, init_db
from models.customer import Customer
from utils.excel_reader import read_users_from_excel
from utils.logger import setup_logger, get_logger
from utils.password import hash_password

logger = get_logger(__name__)


def main():
    setup_logger()
    # データベース初期化
    init_db()
    
    # Excelファイルから読み込み
    users = read_users_from_excel('【一覧】WEB登録顧客管理表.xlsx')
    
    # データベースに登録
    with Session(engine) as session:
        for user in users:
            customer = Customer(
                address=user.address,
                login_name=user.login_name,
                department=user.department,
                name=user.name,
                email=user.email,
                password=hash_password(user.password)
            )
            session.add(customer)
        session.commit()
    
    logger.info(f"{len(users)}件のデータを登録しました")


if __name__ == "__main__":
    main()
