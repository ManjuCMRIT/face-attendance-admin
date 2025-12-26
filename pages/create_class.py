import streamlit as st
from utils.firebase_utils import db
from utils.constants import DEPARTMENTS

def show():
    st.title("🏫 Create New Class")

    dept = st.selectbox("Department", DEPARTMENTS)
    batch = st.text_input("Batch (Year of Admission)", "2024")
    section = st.text_input("Section", "A")

    if st.button("Create Class"):
        class_id = f"{dept}_{batch}_{section}"

        ref = db.collection("classes").document(class_id)
        if ref.get().exists:
            st.warning("Class already exists")
            return

        ref.set({
            "department": dept,
            "batch": batch,
            "section": section
        })

        st.success(f"Class {class_id} created")
        st.session_state["current_class"] = class_id
        st.session_state["page"] = "upload_students"
        st.rerun()
