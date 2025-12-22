# ...existing code...
# todo_app.py

import streamlit as st
import uuid

st.set_page_config(page_title="ToDoリスト", layout="centered")

st.title("📝 ToDoリストアプリ")
st.write("Streamlit 動いています！")

# --------------------
# セッション初期化
# --------------------
if "todos" not in st.session_state:
    # 各要素: {'id': str, 'task': str, 'done': bool}
    st.session_state.todos = []

if "edit_id" not in st.session_state:
    st.session_state.edit_id = None

if "edit_text" not in st.session_state:
    st.session_state.edit_text = ""

# --------------------
# 関数群
# --------------------
def add_todo():
    text = st.session_state.get("new_todo", "").strip()
    if text:
        st.session_state.todos.append({
            "id": str(uuid.uuid4()),
            "task": text,
            "done": False
        })
        st.session_state.new_todo = ""

def delete_todo(todo_id):
    st.session_state.todos = [
        t for t in st.session_state.todos if t["id"] != todo_id
    ]

def toggle_done(todo_id, value):
    for t in st.session_state.todos:
        if t["id"] == todo_id:
            t["done"] = value
            break

def start_edit(todo_id):
    for t in st.session_state.todos:
        if t["id"] == todo_id:
            st.session_state.edit_id = todo_id
            st.session_state.edit_text = t["task"]
            break

def apply_edit():
    for t in st.session_state.todos:
        if t["id"] == st.session_state.edit_id:
            if st.session_state.edit_text.strip():
                t["task"] = st.session_state.edit_text.strip()
            break
    st.session_state.edit_id = None
    st.session_state.edit_text = ""

def cancel_edit():
    st.session_state.edit_id = None
    st.session_state.edit_text = ""

def clear_done():
    st.session_state.todos = [
        t for t in st.session_state.todos if not t["done"]
    ]

# --------------------
# 入力エリア（Enterで追加）
# --------------------
st.text_input(
    "新しいタスクを入力して Enter",
    key="new_todo",
    on_change=add_todo,
    placeholder="例: レポートをまとめる"
)

st.markdown("---")

# --------------------
# 編集エリア
# --------------------
if st.session_state.edit_id is not None:
    st.subheader("✏️ タスクを編集")
    st.text_input("編集内容", key="edit_text")
    col1, col2 = st.columns(2)
    with col1:
        st.button("更新", on_click=apply_edit)
    with col2:
        st.button("キャンセル", on_click=cancel_edit)
    st.markdown("---")

# --------------------
# タスク一覧
# --------------------
st.subheader(f"📋 タスク一覧（合計: {len(st.session_state.todos)}）")

if not st.session_state.todos:
    st.info("タスクがありません。")
else:
    delete_id = None

    for t in st.session_state.todos:
        cols = st.columns([0.7, 0.15, 0.15])

        done = cols[0].checkbox(
            t["task"],
            value=t["done"],
            key=f"chk_{t['id']}"
        )
        if done != t["done"]:
            toggle_done(t["id"], done)

        if cols[1].button("編集", key=f"edit_{t['id']}"):
            start_edit(t["id"])

        if cols[2].button("削除", key=f"del_{t['id']}"):
            delete_id = t["id"]

    if delete_id is not None:
        delete_todo(delete_id)

st.markdown("---")

# --------------------
# 一括操作
# --------------------
col1, col2 = st.columns(2)
with col1:
    st.button("完了済みを一括削除", on_click=clear_done)
with col2:
    if st.button("全件クリア"):
        st.session_state.todos = []
