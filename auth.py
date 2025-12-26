import streamlit as st

def admin_login():
    st.title("🔐 Admin Login")

    password = st.text_input("Enter Admin Password", type="password")

    if st.button("Login"):
        if password == st.secrets["ADMIN_PASSWORD"]:
            st.session_state["logged_in"] = True
            st.session_state["page"] = "dashboard"
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid password")
