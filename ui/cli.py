from services.customer_import import CustomerImportService
from utils.logger import setup_logger, get_logger

logger = get_logger(__name__)


def main():
    """CUIでの顧客データインポート"""
    setup_logger()
    
    service = CustomerImportService()
    
    print("\n" + "="*50)
    print("顧客データインポートツール (CUI)")
    print("="*50)
    
    file_path = input("\nExcelファイルのパスを入力してください: ")
    
    try:
        print("\n読み込み中...")
        users = service.load_from_excel(file_path)
        
        print("差分チェック中...")
        new_users, existing_users = service.check_diff(users)
        
        print(f"\n新規: {len(new_users)}件")
        print(f"登録済: {len(existing_users)}件")
        print(f"合計: {len(users)}件")
        
        if len(new_users) == 0:
            print("\n新規データがありません。")
            return
        
        print("\n新規データ (最初の5件):")
        for i, user in enumerate(new_users[:5], 1):
            print(f"  {i}. {user.name} ({user.email})")
        
        confirm = input("\nデータベースに登録しますか? (y/n): ")
        
        if confirm.lower() == 'y':
            print("\n登録中...")
            count = service.import_customers(new_users)
            print(f"✓ {count}件のデータを登録しました")
        else:
            print("キャンセルしました")
    
    except Exception as ex:
        logger.error(f"エラー: {ex}")
        print(f"\nエラー: {ex}")


if __name__ == "__main__":
    main()
