import streamlit as st
from utils.firebase_utils import db

def show():
    st.title("📂 Manage Classes")

    classes = db.collection("classes").stream()

    for cls in classes:
        data = cls.to_dict()
        label = f"{data['department']} - {data['batch']} - {data['section']}"

        if st.button(label):
            st.session_state["current_class"] = cls.id
            st.session_state["page"] = "class_details"
            st.rerun()

