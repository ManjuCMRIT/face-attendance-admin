import streamlit as st
from utils.firebase_utils import db

def show():
    st.title("🔗 Map Old Embeddings to USN (Manual Linking)")

    st.info("""
    Use this tool to assign old embeddings to newly uploaded student list.
    Works even if names don't match exactly. Map manually one by one.
    """)

    # ---------------- Class Selection ----------------
    dept = st.selectbox("Department", ["CSE","ISE","AI/ML","CS-ML","CS-DS","AI/DS","MBA","MCA"])
    batch = st.text_input("Batch (Year)", "2024")
    section = st.text_input("Section", "B")

    class_id = f"{dept}_{batch}_{section}"

    if st.button("Load Student List"):
        # Load class students
        students = db.collection("classes").document(class_id).collection("students").stream()
        st.session_state.students = {s.id: s.to_dict() for s in students}

        # Load old embeddings
        old_users = db.collection("users").stream()
        st.session_state.old_users = {u.id: u.to_dict() for u in old_users}

        st.success(f"Loaded Class: {class_id}")
        st.write(f"Students found: {len(st.session_state.students)}")
        st.write(f"Old registered embeddings found: {len(st.session_state.old_users)}")


    # ---------------- Manual Mapping Section ----------------
    if "students" in st.session_state:

        st.subheader("🧠 Manual Mapping Panel")
        st.caption("Match each student USN → old name → save embedding")

        old_names = list(st.session_state.old_users.keys())   # names from old db

        for usn, data in st.session_state.students.items():
            name = data['name']

            st.markdown(f"### 👤 {name} — `{usn}`")

            # Dropdown to manually select matching old name
            selected = st.selectbox(
                "Select old registered name to map",
                ["--Select--"] + old_names,
                key=f"select_{usn}"
            )

            if selected != "--Select--":
                embedding = st.session_state.old_users[selected]["embedding"]

                if st.button("Map Embedding", key=f"map_{usn}"):
                    db.collection("classes").document(class_id)\
                        .collection("students").document(usn).update({
                            "embedding": embedding,
                            "face_registered": True
                        })

                    st.success(f"✔ Mapped: **{selected} → {name} ({usn})**")
                    st.balloons()

            st.markdown("---")
