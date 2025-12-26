import streamlit as st
from auth import admin_login
from pages import dashboard, create_class, upload_students, manage_classes, class_details

st.set_page_config("Admin Dashboard", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "page" not in st.session_state:
    st.session_state["page"] = "login"

if not st.session_state["logged_in"]:
    admin_login()
else:
    page = st.session_state["page"]

    if page == "dashboard":
        dashboard.show()
    elif page == "create_class":
        create_class.show()
    elif page == "upload_students":
        upload_students.show()
    elif page == "manage_classes":
        manage_classes.show()
    elif page == "class_details":
        class_details.show()
