import streamlit as st

def show():
    st.title("📊 Admin Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ Create New Class"):
            st.session_state["page"] = "create_class"
            st.rerun()

    with col2:
        if st.button("📂 Manage Existing Classes"):
            st.session_state["page"] = "manage_classes"
            st.rerun()
