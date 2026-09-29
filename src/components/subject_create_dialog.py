import streamlit as st 
from src.database.db import create_subject 

@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the details of new subject")
    sub_name = st.text_input("Enter subject name",placeholder="Computer science")
    sub_code = st.text_input("Enter subject code",placeholder="CS101")
    section = st.text_input("Enter section",placeholder="A")

    if st.button("Create New Subject",type="primary",width="stretch"):
        if sub_name and sub_code and section :
            try:
                create_subject(sub_name,sub_code,section,teacher_id)
                st.toast("Subject created Successfully!")
                st.rerun()
            except Exception as e:
                print(f"Exception : {str(e)}")
        else:
            st.warning("Please enter all details")