import streamlit as st
import uuid


if "tasks" not in st.session_state:
    st.session_state.tasks = []



st.title("📝 To-Do List")

new_task = st.text_input("Enter a task")

if st.button("Add Task"):
    if new_task.strip():
        st.session_state.tasks.append({
            "id": str(uuid.uuid4()),
            "title": new_task
        })
        st.rerun()



st.subheader("Tasks")

if st.session_state.tasks:
    for task in st.session_state.tasks:
        col1, col2 = st.columns([5, 1])

        with col1:
            st.write(task["title"])

        with col2:
            if st.button("🗑️", key=task["id"]):
                st.session_state.tasks = [
                    t for t in st.session_state.tasks
                    if t["id"] != task["id"]
                ]
                st.rerun()
else:
    st.info("No tasks yet")