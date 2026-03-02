import flet as ft
from services.customer_import import CustomerImportService
from utils.logger import setup_logger, get_logger
from exceptions import ExcelFormatError
from ui.components import ExcelFilePicker

logger = get_logger(__name__)


def create_app(page: ft.Page):
    """Flet GUIアプリケーションを作成"""
    setup_logger()
    page.title = "顧客データインポート"
    page.window.width = 700
    page.window.height = 500
    page.padding = 20
    page.splash = None  # スプラッシュを非表示にする場合
    service = CustomerImportService()

    status_text = ft.Text("ファイルを選択してください", size=16)
    progress_bar = ft.ProgressBar(visible=False)
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("状態")),
            ft.DataColumn(ft.Text("担当営業所")),
            ft.DataColumn(ft.Text("担当者")),
            ft.DataColumn(ft.Text("会社名")),
            ft.DataColumn(ft.Text("メール")),
        ],
        rows=[],
        visible=False,
    )

    def on_excel_uploaded(file_path: str):
        """Excelファイルアップロード完了時の処理"""
        try:
            status_text.value = "読み込み中..."
            progress_bar.visible = True
            page.update()

            users = service.load_from_excel(file_path)
            new_users, existing_users = service.check_diff(users)

            # テーブルに表示
            data_table.rows.clear()

            for user in new_users[:10]:
                data_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text("新規", color=ft.colors.GREEN),
                                    bgcolor=ft.colors.GREEN_100,
                                    padding=5,
                                    border_radius=5,
                                )
                            ),
                            ft.DataCell(ft.Text(user.in_charge)),
                            ft.DataCell(ft.Text(user.name)),
                            ft.DataCell(ft.Text(user.company_name)),
                            ft.DataCell(ft.Text(user.email)),
                        ]
                    )
                )

            for user in existing_users[:5]:
                data_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text("登録済", color=ft.colors.GREY),
                                    bgcolor=ft.colors.GREY_200,
                                    padding=5,
                                    border_radius=5,
                                )
                            ),
                            ft.DataCell(ft.Text(user.in_charge)),
                            ft.DataCell(ft.Text(user.name)),
                            ft.DataCell(ft.Text(user.company_name)),
                            ft.DataCell(ft.Text(user.email)),
                        ]
                    )
                )

            data_table.visible = True
            status_text.value = f"新規: {len(new_users)}件 / 登録済: {len(existing_users)}件 / 合計: {len(users)}件"
            import_button.visible = len(new_users) > 0
            import_button.data = new_users
            progress_bar.visible = False
            page.update()

        except ExcelFormatError as ex:
            status_text.value = f"フォーマットエラー: {str(ex)}"
            progress_bar.visible = False
            logger.error(f"Excelフォーマットエラー: {ex}")
            page.update()
        except FileNotFoundError as ex:
            status_text.value = f"ファイルエラー: {str(ex)}"
            progress_bar.visible = False
            logger.error(f"ファイルが見つかりません: {ex}")
            page.update()
        except Exception as ex:
            status_text.value = f"エラー: {str(ex)}"
            progress_bar.visible = False
            logger.exception(f"ファイル処理エラー: {ex}")
            page.update()

    def on_excel_error(ex: Exception):
        """エラーハンドラー"""
        status_text.value = f"エラー: {str(ex)}"
        progress_bar.visible = False
        page.update()

    def on_import_clicked(e):
        try:
            users = e.control.data
            status_text.value = "データベースに登録中..."
            progress_bar.visible = True
            import_button.disabled = True
            page.update()

            count = service.import_customers(users)

            status_text.value = f"✓ {count}件のデータを登録しました"
            progress_bar.visible = False
            import_button.visible = False
            page.update()

        except Exception as ex:
            status_text.value = f"エラー: {str(ex)}"
            progress_bar.visible = False
            import_button.disabled = False
            logger.error(f"インポートエラー: {ex}")
            page.update()

    excel_picker = ExcelFilePicker(
        page=page,
        on_upload_complete=on_excel_uploaded,
        on_error=on_excel_error,
    )
    page.overlay.append(excel_picker.get_control())

    import_button = ft.ElevatedButton(
        "データベースに登録",
        icon=ft.icons.UPLOAD,
        on_click=on_import_clicked,
        visible=False,
    )

    page.add(
        ft.Column(
            [
                ft.Text(
                    "顧客データインポートツール", size=24, weight=ft.FontWeight.BOLD
                ),
                ft.Divider(),
                ft.ElevatedButton(
                    "ファイルを選択",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=lambda _: excel_picker.pick_files(),
                ),
                status_text,
                progress_bar,
                import_button,
                ft.Container(
                    content=ft.Column([data_table], scroll=ft.ScrollMode.AUTO),
                    height=250,
                ),
            ],
            spacing=10,
        )
    )
