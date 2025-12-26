import streamlit as st
from utils.firebase_utils import db

def show():
    class_id = st.session_state.get("current_class")
    st.title(f"🏫 {class_id}")

    students = db.collection("classes").document(class_id).collection("students").stream()

    data = []
    for s in students:
        d = s.to_dict()
        data.append({
            "USN": d["usn"],
            "Name": d["name"],
            "Face Registered": d["face_registered"]
        })

    st.dataframe(data)
