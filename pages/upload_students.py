import streamlit as st
import pandas as pd
from utils.firebase_utils import db

def show():
    st.title("📄 Upload Student List")

    class_id = st.session_state.get("current_class")
    if not class_id:
        st.error("No class selected")
        return

    file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

    if file:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        st.dataframe(df)

        if st.button("Confirm & Save"):
            users_ref = db.collection("users")

            registered = 0
            pending = 0

            for _, row in df.iterrows():
                usn = row["USN"]
                name = row["Name"]

                user_doc = users_ref.document(usn).get()

                student_data = {
                    "usn": usn,
                    "name": name,
                    "face_registered": user_doc.exists
                }

                if user_doc.exists:
                    student_data["embedding"] = user_doc.to_dict()["embedding"]
                    registered += 1
                else:
                    pending += 1

                db.collection("classes") \
                  .document(class_id) \
                  .collection("students") \
                  .document(usn) \
                  .set(student_data)

            st.success(f"{registered} registered, {pending} pending")
