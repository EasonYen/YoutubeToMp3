# Youtube to MP3 Converter

> 🎓 **這是一個學習專案**，用於練習 Python GUI 開發（Flet 框架）與多媒體處理。

一個簡單的桌面應用程式，可以將 Youtube 影片下載並轉換為 MP3 格式。

## ⚠️ 免責聲明 (Disclaimer)

**本專案僅供個人學習與技術研究使用，不鼓勵任何侵犯著作權的行為。**

- 📚 本工具是一個 **Python + Flet GUI 開發練習專案**
- 🔧 核心下載功能依賴開源工具 [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- ⚖️ 使用者應確保僅下載自己擁有權利的內容，或已獲得授權的內容
- 📜 請遵守當地著作權法規及 YouTube 服務條款
- 🙅 開發者不對任何濫用行為負責

**下載受版權保護的內容可能違反當地法律。請尊重內容創作者的權益。**

---

## 功能
- 下載 Youtube 影片
- 自動轉換為高品質 MP3 (192kbps)
- 支援 Windows, macOS, Linux
- 自動偵測 FFmpeg
- 即時顯示下載進度與速度

## 技術棧
- **Python 3.12**
- **Flet 0.25.x** - 跨平台 GUI 框架
- **yt-dlp** - YouTube 下載函式庫
- **FFmpeg** - 音訊處理
- **PyInstaller** - 應用程式打包

## 開發環境設定

1. 安裝 Python 3.8+（建議 3.12）
2. 建立虛擬環境：
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   # 或 venv\Scripts\activate  # Windows
   ```
3. 安裝相依套件：
   ```bash
   pip install -r requirements.txt
   ```

## 執行程式

```bash
python src/main.py
```

## 打包為執行檔

本專案提供了一個打包腳本，方便您將程式打包為執行檔。

```bash
python build.py
```

打包完成後，執行檔將位於 `dist` 資料夾中：
- macOS: `dist/YoutubeToMp3.app`
- Windows: `dist/YoutubeToMp3.exe`

## 注意事項
- 本程式依賴 `FFmpeg`。如果系統未安裝，程式啟動時會提示安裝。
- macOS 用戶可透過 `brew install ffmpeg` 安裝
- Windows 用戶請從 [FFmpeg 官網](https://ffmpeg.org/download.html) 下載

## 學習重點

這個專案涵蓋了以下技術實作：

1. **Flet GUI 開發** - 使用 Python 建立跨平台桌面應用
2. **多執行緒處理** - 背景下載不阻塞 UI
3. **跨執行緒 UI 更新** - 使用共享狀態模式安全更新介面
4. **第三方 API 整合** - 封裝 yt-dlp 函式庫
5. **應用程式打包** - 使用 PyInstaller 建立獨立執行檔

## License

MIT License - 詳見 [LICENSE](LICENSE) 檔案

---

*此專案僅用於教育目的。請負責任地使用。*
