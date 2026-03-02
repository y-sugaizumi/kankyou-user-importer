import flet as ft
from typing import Callable
from utils.logger import get_logger

logger = get_logger(__name__)


class ExcelFilePicker:
    """Excelファイル選択用のカスタムFilePicker"""
    
    def __init__(
        self,
        page: ft.Page,
        on_upload_complete: Callable[[str], None],
        on_error: Callable[[Exception], None] = None,
    ):
        self.page = page
        self.on_upload_complete_callback = on_upload_complete
        self.on_error_callback = on_error
        
        self.picker = ft.FilePicker(
            on_result=self._on_file_selected,
            on_upload=self._on_upload_complete,
        )
    
    def _on_file_selected(self, e: ft.FilePickerResultEvent):
        """ファイル選択時の処理"""
        if e.files:
            file = e.files[0]
            logger.info(f"ファイル選択: {file.name}")
            
            try:
                upload_list = [
                    ft.FilePickerUploadFile(
                        file.name,
                        upload_url=self.page.get_upload_url(file.name, 600),
                    )
                ]
                self.picker.upload(upload_list)
            except Exception as ex:
                logger.error(f"アップロード開始エラー: {ex}")
                if self.on_error_callback:
                    self.on_error_callback(ex)
    
    def _on_upload_complete(self, e: ft.FilePickerUploadEvent):
        """アップロード完了時の処理"""
        try:
            file_path = f"uploads/{e.file_name}"
            logger.info(f"アップロード完了: {file_path}")
            self.on_upload_complete_callback(file_path)
        except Exception as ex:
            logger.exception(f"アップロード完了処理エラー: {ex}")
            if self.on_error_callback:
                self.on_error_callback(ex)
    
    def pick_files(self):
        """ファイル選択ダイアログを開く"""
        self.picker.pick_files(allowed_extensions=["xlsx"])
    
    def get_control(self) -> ft.FilePicker:
        """FilePickerコントロールを取得"""
        return self.picker
