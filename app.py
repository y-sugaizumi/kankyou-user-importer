import flet as ft
from ui.flet_app import create_app
import os

if __name__ == "__main__":
    os.environ["FLET_SECRET_KEY"] = "my-secret-key-for-upload"
    ft.app(
        target=create_app,
        view=ft.AppView.WEB_BROWSER,
        assets_dir="assets",
        upload_dir="uploads",
    )
else:
    # gunicorn/uvicorn用のASGIアプリケーション
    os.environ["FLET_SECRET_KEY"] = "my-secret-key-for-upload"
    app = ft.app(
        target=create_app,
        assets_dir="assets",
        upload_dir="uploads",
    )
