import streamlit as st
from utils.firebase_utils import db

st.title("🔄 Map Old Embeddings from `users` to Class Students")

st.warning("⚠ One-time use page for migrating old registered faces.\n"
           "Make sure student names in CSV match names in `users`.")

# Input Class
dept = st.selectbox("Department", ["CSE","ISE","AI/ML","CS-ML","CS-DS","AI/DS","MBA","MCA"])
batch = st.text_input("Batch (Year of Admission)", "2024")
section = st.text_input("Section", "B")

if st.button("Load Students"):
    class_id = f"{dept}_{batch}_{section}"
    st.session_state.class_id = class_id
    
    # Load students under class
    students = db.collection("classes").document(class_id).collection("students").stream()
    students = {s.id:s.to_dict() for s in students}
    
    # Load old embeddings
    old_users = db.collection("users").stream()
    old_users = {u.id:u.to_dict() for u in old_users}
    
    st.success(f"Loaded Class: {class_id}")
    
    # Store in session
    st.session_state.students = students
    st.session_state.old_users = old_users


if "students" in st.session_state:
    st.subheader("🧠 Match Names & Transfer Embeddings")

    for usn, data in st.session_state.students.items():
        name = data['name']

        # If user exists in old system
        if name in st.session_state.old_users:
            embedding = st.session_state.old_users[name]["embedding"]

            col1, col2 = st.columns([3,1])
            col1.write(f"**{name}** ({usn})")

            if col2.button("Map", key=usn):
                db.collection("classes").document(st.session_state.class_id)\
                    .collection("students").document(usn)\
                    .update({"embedding": embedding, "face_registered": True})

                st.success(f"Mapped → {name} ({usn})")

        else:
            st.error(f"❌ No embedding found for {name}")
