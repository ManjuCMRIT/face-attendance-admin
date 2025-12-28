import streamlit as st

def navbar():

    st.markdown("---")
    col1, col2, col3, col4,col5 = st.columns(5)

    if col1.button("🏠 Home"):
        st.session_state["page"] = "dashboard"
        st.rerun()

    if col2.button("➕ Create Class"):
        st.session_state["page"] = "create_class"
        st.rerun()

    if col3.button("📂 Manage Classes"):
        st.session_state["page"] = "manage_classes"
        st.rerun()

    if col4.button("📄 Upload Students"):
        if "current_class" in st.session_state:
            st.session_state["page"] = "upload_students"
            st.rerun()
        else:
            st.warning("Select a class first in Manage Classes")
        # 🔗 new button for mapping embeddings
    if col5.button("🔗 Map Embeddings"):
        st.session_state["page"] = "map_embeddings"
        st.rerun()


    
    st.markdown("---")
