from pathlib import Path
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

# --------------------
# データベース設定
# --------------------
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / 'todos.db'

def get_db_conn():
    return sqlite3.connect(str(DB_PATH))

def init_db():
    conn = get_db_conn()
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0
        )
        """
    )
    conn.commit()
    conn.close()

# --------------------
# Flask アプリ
# --------------------
app = Flask(__name__)

# --------------------
# 一覧表示
# --------------------
@app.route('/')
def index():
    conn = get_db_conn()
    c = conn.cursor()
    c.execute('SELECT id, title, done FROM todos ORDER BY id DESC')
    todos = c.fetchall()
    conn.close()
    return render_template('index.html', todos=todos)

# --------------------
# ToDo 追加
# --------------------
@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title', '').strip()
    if title:
        conn = get_db_conn()
        c = conn.cursor()
        c.execute('INSERT INTO todos (title, done) VALUES (?, 0)', (title,))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

# --------------------
# 完了切り替え
# --------------------
@app.route('/toggle/<int:todo_id>', methods=['POST'])
def toggle(todo_id):
    conn = get_db_conn()
    c = conn.cursor()
    c.execute('UPDATE todos SET done = 1 - done WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# --------------------
# 編集
# --------------------
@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit(todo_id):
    conn = get_db_conn()
    c = conn.cursor()

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        if title:
            c.execute('UPDATE todos SET title = ? WHERE id = ?', (title, todo_id))
            conn.commit()
        conn.close()
        return redirect(url_for('index'))

    c.execute('SELECT id, title, done FROM todos WHERE id = ?', (todo_id,))
    todo = c.fetchone()
    conn.close()

    if todo:
        return render_template('edit.html', todo=todo)
    return redirect(url_for('index'))

# --------------------
# 削除
# --------------------
@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete(todo_id):
    conn = get_db_conn()
    c = conn.cursor()
    c.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# --------------------
# 起動
# --------------------
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='127.0.0.1', port=5000)
