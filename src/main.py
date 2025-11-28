import flet as ft
import os
import threading
from utils import check_ffmpeg_installed, get_ffmpeg_install_guide
from downloader import YoutubeDownloader

def main(page: ft.Page):
    page.title = "Youtube to MP3 Converter"
    page.window_width = 650
    page.window_height = 580
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    # --- State Variables ---
    selected_folder = ft.Ref[str]()
    download_status = ft.Ref[ft.Text]()
    progress_bar = ft.Ref[ft.ProgressBar]()
    url_input = ft.Ref[ft.TextField]()
    quality_dropdown = ft.Ref[ft.Dropdown]()
    ffmpeg_path_ref = ft.Ref[str]()
    
    # 共享進度狀態
    progress_state = {"value": 0, "text": "準備中...", "updated": False}
    
    # Default folder to user's downloads or home
    default_path = os.path.expanduser("~/Downloads")
    selected_folder.current = default_path

    # --- Event Handlers ---
    
    def on_dialog_result(e: ft.FilePickerResultEvent):
        if e.path:
            selected_folder.current = e.path
            folder_text.value = e.path
            page.update()

    file_picker = ft.FilePicker(on_result=on_dialog_result)
    page.overlay.append(file_picker)

    def clean_ansi(text):
        """移除 ANSI 顏色碼和特殊字元"""
        import re
        if not text:
            return ""
        # 移除 ANSI escape sequences
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', str(text)).strip()

    def progress_hook(d):
        status = d.get('status', '')
        
        try:
            if status == 'downloading':
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                speed = d.get('speed', 0)
                
                # 計算進度
                if total > 0:
                    progress = downloaded / total
                else:
                    progress = 0
                
                # 格式化顯示文字
                percent_display = f"{progress * 100:.1f}%"
                
                if speed and speed > 0:
                    if speed >= 1024 * 1024:
                        speed_display = f"{speed / (1024 * 1024):.1f} MB/s"
                    elif speed >= 1024:
                        speed_display = f"{speed / 1024:.1f} KB/s"
                    else:
                        speed_display = f"{speed:.0f} B/s"
                else:
                    speed_display = "計算中..."
                
                # 更新共享狀態
                progress_state["value"] = min(progress, 1.0)
                progress_state["text"] = f"下載中... {percent_display} (速度: {speed_display})"
                progress_state["updated"] = True
                
            elif status == 'finished':
                progress_state["value"] = 1.0
                progress_state["text"] = "下載完成，正在轉檔..."
                progress_state["updated"] = True
        except Exception as ex:
            print(f"[DEBUG] progress_hook error: {ex}")

    def update_progress_ui():
        """定時檢查並更新 UI"""
        if progress_state["updated"]:
            progress_bar.current.value = progress_state["value"]
            download_status.current.value = progress_state["text"]
            progress_state["updated"] = False
            page.update()

    def start_download(e):
        url = url_input.current.value
        if not url:
            url_input.current.error_text = "請輸入影片網址"
            url_input.current.update()
            return
        
        if "youtube.com" not in url and "youtu.be" not in url:
            url_input.current.error_text = "請輸入有效的 Youtube 影片網址"
            url_input.current.update()
            return
        
        url_input.current.error_text = None
        download_btn.disabled = True
        progress_bar.current.visible = True
        download_status.current.value = "準備中..."
        page.update()

        downloader = YoutubeDownloader()
        
        # 用於停止進度更新的標記
        download_running = {"active": True}
        
        def progress_updater():
            """每 200ms 更新一次 UI"""
            import time
            while download_running["active"]:
                update_progress_ui()
                time.sleep(0.2)
        
        def download_task():
            success, message = downloader.download_video_as_mp3(
                url, 
                selected_folder.current, 
                quality_dropdown.current.value, 
                progress_hook,
                ffmpeg_path=ffmpeg_path_ref.current
            )
            
            download_running["active"] = False  # 停止進度更新
            
            if success:
                download_status.current.value = "成功！檔案已儲存。"
                progress_bar.current.value = 0
                progress_bar.current.visible = False
                url_input.current.value = ""
                page.show_snack_bar(ft.SnackBar(content=ft.Text("下載成功！")))
            else:
                download_status.current.value = f"錯誤: {message}"
                progress_bar.current.visible = False
            
            download_btn.disabled = False
            page.update()

        # 啟動進度更新執行緒和下載執行緒
        threading.Thread(target=progress_updater, daemon=True).start()
        threading.Thread(target=download_task, daemon=True).start()

    # --- UI Components ---

    title = ft.Text("Youtube to MP3", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.RED)
    
    url_input_control = ft.TextField(
        ref=url_input,
        label="Youtube 影片網址",
        hint_text="https://www.youtube.com/watch?v=...",
        width=500,
        prefix_icon=ft.icons.LINK
    )

    folder_text = ft.Text(value=default_path, expand=True)
    folder_btn = ft.ElevatedButton(
        "選擇資料夾", 
        icon=ft.icons.FOLDER_OPEN, 
        on_click=lambda _: file_picker.get_directory_path()
    )
    
    quality_dropdown_control = ft.Dropdown(
        ref=quality_dropdown,
        label="音質 (Bitrate)",
        width=200,
        options=[
            ft.dropdown.Option("128", "128 kbps (標準)"),
            ft.dropdown.Option("192", "192 kbps (高)"),
            ft.dropdown.Option("320", "320 kbps (極高)"),
        ],
        value="192"
    )

    download_btn = ft.ElevatedButton(
        "開始下載",
        icon=ft.icons.DOWNLOAD,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.RED,
            padding=20,
        ),
        on_click=start_download,
        width=200
    )

    progress_bar_control = ft.ProgressBar(ref=progress_bar, width=500, visible=False, value=0)
    status_text = ft.Text(ref=download_status, value="準備就緒")

    # --- Layout ---
    
    main_view = ft.Column(
        controls=[
            ft.Container(height=20),
            ft.Row([title], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=20),
            ft.Row([url_input_control], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=10),
            ft.Row([
                ft.Container(content=folder_text, padding=10, border=ft.border.all(1, ft.colors.GREY_400), border_radius=5, expand=True),
                folder_btn
            ], width=500, alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=10),
            ft.Row([quality_dropdown_control], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=30),
            ft.Row([download_btn], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=20),
            ft.Row([progress_bar_control], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([status_text], alignment=ft.MainAxisAlignment.CENTER),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # --- FFmpeg Check ---
    
    def check_ffmpeg_and_start():
        ffmpeg_path = check_ffmpeg_installed()
        if not ffmpeg_path:
            guide = get_ffmpeg_install_guide()
            
            def close_dialog(e):
                # Re-check
                path = check_ffmpeg_installed()
                if path:
                    ffmpeg_path_ref.current = path
                    dlg.open = False
                    page.update()
                else:
                    # Show error or just stay open
                    pass

            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("未偵測到 FFmpeg"),
                content=ft.Column([
                    ft.Text("本工具需要 FFmpeg 才能進行轉檔。"),
                    ft.Text(f"您的系統是: {guide['os']}"),
                    ft.Text("請依照以下方式安裝："),
                    ft.Container(
                        content=ft.Text(guide['command'], font_family="monospace", selectable=True),
                        bgcolor=ft.colors.GREY_200,
                        padding=10
                    ),
                    ft.TextButton("開啟下載頁面", on_click=lambda e: page.launch_url(guide['url'])),
                ], height=200, width=400),
                actions=[
                    ft.TextButton("我已安裝，重試", on_click=close_dialog),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.dialog = dlg
            dlg.open = True
            page.update()
        else:
            ffmpeg_path_ref.current = ffmpeg_path
            pass

    page.add(main_view)
    
    # Run check after UI is built
    check_ffmpeg_and_start()

if __name__ == "__main__":
    ft.app(target=main)
