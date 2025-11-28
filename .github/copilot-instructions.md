# Copilot Instructions for YoutubeToMp3

## 專案架構
- 桌面應用程式，使用 [Flet](https://flet.dev/) 0.25.x 建構 GUI，主程式在 `src/main.py`。
- 下載與轉檔邏輯集中於 `src/downloader.py`，封裝為 `YoutubeDownloader` 類別。
- 工具函式如 FFmpeg 檢查與安裝說明在 `src/utils.py`。
- 測試下載流程可參考 `test_download.py`。
- 打包腳本為 `build.py`，使用 PyInstaller，需先產生 icon 檔（`create_icon.py`）。

## 關鍵開發流程
- **Python 版本**：需使用 Python 3.8+（建議 3.12），yt-dlp 最新版不支援 Python 3.7。
- **虛擬環境**：專案使用 `venv312` 虛擬環境。
- **安裝相依套件**：`pip install -r requirements.txt`
- **執行主程式**：`source venv312/bin/activate && python src/main.py`
- **打包執行檔**：`python build.py`，產物於 `dist/YoutubeToMp3.app`（macOS）。
- **測試下載**：`python test_download.py`（需 FFmpeg）。

## 重要慣例與注意事項
- **FFmpeg 檢查**：啟動時自動偵測，若未安裝會提示安裝。
- **下載品質**：預設 MP3 音質為 192kbps，可於 `downloader.py` 調整。
- **跨平台支援**：Windows/macOS/Linux，icon 檔案需依平台選擇（`.ico`/`.png`）。
- **yt-dlp 關鍵設定**：
  - 使用 `player_client: ['ios', 'android']` 避免 YouTube HTTP 400 錯誤
  - 加入 `User-Agent` header 與重試機制 (`retries: 10`)
  - 兩處同步：`downloader.py` 與 `test_download.py`
- **Flet 版本注意事項**：
  - 使用 Flet 0.25.x（0.28+ 在 macOS 上 FilePicker 有問題）
  - API 使用小寫 `ft.colors`, `ft.icons`（非大寫）
  - SnackBar 使用 `page.show_snack_bar()` 方法
- **跨執行緒 UI 更新**：
  - 使用共享狀態字典 + 獨立更新執行緒來更新進度
  - 不可直接從子執行緒呼叫 `page.update()`

## 外部整合
- 依賴 `yt-dlp` 進行 YouTube 下載與音訊轉檔（需最新版本）。
- 依賴 `FFmpeg` 進行音訊處理，路徑自動偵測，常見路徑已在 `utils.py` 處理。

## 典型程式碼範例
```python
# 下載並轉檔
from downloader import YoutubeDownloader
downloader = YoutubeDownloader()
downloader.download_video_as_mp3(url, output_folder, quality='192')
```

## 參考檔案
- `src/main.py`：主 GUI 與流程
- `src/downloader.py`：下載/轉檔邏輯
- `src/utils.py`：FFmpeg 檢查/安裝
- `build.py`：打包腳本
- `test_download.py`：下載測試
- `requirements.txt`：相依套件
- `venv312/`：Python 3.12 虛擬環境

---
如有不清楚或未涵蓋的部分，請回饋以便補充！