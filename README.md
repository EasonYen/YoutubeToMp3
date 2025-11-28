# Youtube to MP3 Converter

這是一個簡單的桌面應用程式，可以將 Youtube 影片下載並轉換為 MP3 格式。

## 功能
- 下載 Youtube 影片
- 自動轉換為高品質 MP3
- 支援 Windows, macOS, Linux
- 自動偵測 FFmpeg

## 開發環境設定

1. 安裝 Python 3.10+
2. 安裝相依套件：
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

打包完成後，執行檔將位於 `dist` 資料夾中。

## 注意事項
- 本程式依賴 `FFmpeg`。如果系統未安裝，程式啟動時會提示安裝。
