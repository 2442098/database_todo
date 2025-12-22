FROM python:3.11-slim

WORKDIR /app

# 依存パッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリ本体をコンテナにコピー
COPY . .

# Streamlit のデフォルトポート
EXPOSE 8501

# Streamlit アプリを起動
CMD ["streamlit", "run", "app/todo_app.py", "--server.port=8501", "--server.address=0.0.0.0"]