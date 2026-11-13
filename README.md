# LINE Messaging API 教學文件

本專案是「專業排版與設計」期中考作業，使用繁體中文 LaTeX 撰寫 LINE Messaging API 註冊、Webhook 設定與 Python Echo Bot 教學文件。

## 編譯 PDF

需要安裝 MiKTeX 與 XeLaTeX：

```powershell
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

重複編譯是為了更新目錄、圖表目錄與程式目錄。完成後產生 `main.pdf`。

## 執行範例

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python app.py
```

請將 `.env` 中的兩個值替換為 LINE Developers Console 的實際認證資料，並使用 ngrok 將 `http://localhost:8000` 暫時公開為 HTTPS。

## Git 版本控管

本文件應保留至少三個有效提交：文件架構、Echo Bot 程式、最終排版與測試說明。推送到 GitHub 前，確認 `.env` 沒有被加入版本庫：

```powershell
git status
git log --oneline --decorate -3
git remote add origin https://github.com/你的帳號/line-messaging-api-report.git
git branch -M main
git push -u origin main
```

## 檔案說明

- `main.tex`：完整 LaTeX 文件，最後一章會以 `lstinputlisting` 收錄自身原始碼。
- `app.py`：Flask + LINE Bot SDK v3 Echo Bot。
- `requirements.txt`：Python 依賴。
- `.gitignore`：排除機密資料、虛擬環境與 LaTeX 暫存檔。
