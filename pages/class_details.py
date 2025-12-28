import streamlit as st
from utils.firebase_utils import db, bucket
from components.navbar import navbar
def show():
    navbar()
    class_id = st.session_state.get("current_class")
    st.title(f"🏫 Class: {class_id}")

    students = db.collection("classes").document(class_id).collection("students").stream()

    for s in students:
        d = s.to_dict()
        col1, col2, col3 = st.columns([2,1,2])

        with col1:
            st.write(f"**{d['usn']} - {d['name']}**")

        with col2:
            status = "🟢 Registered" if d.get("face_registered") else "🔴 Pending"
            st.write(status)

        with col3:
            if d.get("face_registered"):
                
                if st.button(f"Delete Face ({d['usn']})"):
                    # Delete embedding & mark pending
                    db.collection("classes").document(class_id)\
                       .collection("students").document(d['usn']).update({
                           "face_registered": False,
                           "embedding": None
                       })
                    
                    # Remove image file from bucket if exists
                    try:
                        img_blob = bucket.blob(f"faces/{class_id}/{d['usn']}.jpg")
                        img_blob.delete()
                    except:
                        pass

                    st.success(f"Face deleted for {d['usn']}. Student can re-register now.")
                    st.rerun()

            else:
                st.write("No face registered yet")
