import streamlit as st 
from src.components.header import header_dashboard
from src.ui.base_layout import style_background_dasboard,style_base_layout
from src.components.footer import dashboard_footer
from src.components.subject_create_dialog import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.subject_card import subject_card
from src.database.db import check_teacher_exists,create_teacher,teacher_login,get_teacher_subjects

def teacher_screen():

    style_background_dasboard()
    style_base_layout()

    if 'teacher_data' in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()

def teacher_dashboard():
    teacher = st.session_state.teacher_data

    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f""" Welcome  {teacher["name"]}""")
        if st.button("Logout",shortcut='control+backspace',type='secondary',key='loginbckbtn'):
            st.session_state['is_logged_in']=False
            del st.session_state.teacher_data
            st.rerun()

    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendence"

    tab1,tab2,tab3 = st.columns(3)

    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
        if st.button('Take Attendance',type=type1, width='stretch', icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == "manage_subjects" else "tertiary"
        if st.button("Manage_subjects",type=type2, width='stretch', icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab='manage_subjects'
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == "attendence_records" else "tertiary"
        if st.button("Attendence_records",type=type3, width='stretch', icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab='attendence_records'
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_dashboard_take_attendence()
    elif st.session_state.current_teacher_tab == "manage_subjects":
        teacher_dashboard_manage_subjects()
    elif st.session_state.current_teacher_tab == "attendence_records":
        teacher_dashboard_attendence_records()

    st.space()
    dashboard_footer()


def teacher_dashboard_take_attendence():
    st.header("Take AI Attendence")
     
def teacher_dashboard_manage_subjects():
    teacher_id = st.session_state.teacher_data["teacher_id"]
    col1,col2 = st.columns(2)
    with col1:
        st.header("Manage Subjects",width="content")
    with col2:
        if st.button("Create New Subject",type="secondary",width="stretch"):
            create_subject_dialog(teacher_id)

    #List all Subjects
    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("🫂","Students",sub['total_students']),
                ("🕰️","Classes",sub['total_classes'])
            ]
        def share_btn():
            if st.button(f"Share Code: {sub['name']}",key=f"share_{sub['subject_code']}",icon=':material/share:'):
                share_subject_dialog(sub['name'],sub["subject_code"])
            
            st.space()

        subject_card(
            name=sub['name'],
            code=sub['subject_code'],
            section=sub['section'],
            stats= stats,
            footer_callback=share_btn
        )
    else:
        st.info("NO SUBJECTS FOUND,Create one Above")

def teacher_dashboard_attendence_records():
    st.header("Attendence Records")

def login_teacher(teacher_username,teacher_password):
    if not(teacher_username) or not(teacher_password):
        return False
    
    teacher = teacher_login(teacher_username,teacher_password)

    if teacher:
        st.session_state.teacher_data = teacher
        st.session_state.user_role = "teacher"
        st.session_state.is_logged_in = True 
        return True
    
    return False 

def teacher_register(teacher_username,teacher_name,teacher_password,teacher_pass_confim):
    if not(teacher_username) or not(teacher_name) or not(teacher_password):
        return False,"All Fields required"
    if check_teacher_exists(teacher_username):
        return False,"Username Already taken"
    if teacher_password != teacher_pass_confim:
        return False,"Password doesn't match"
    
    try:
        create_teacher(teacher_username,teacher_password,teacher_name)
        return True,"Successfully profile created"
    except Exception as e:
        return False,"Unexpected Error!"

def teacher_screen_login():
    
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go to Home",shortcut='control+backspace',type='secondary',key='loginbckbtn'):
            st.session_state['login_type']=None
            st.rerun()

    st.header("Login using password",text_alignment='center')
    
    st.space()

    teacher_username = st.text_input("Enter username",width="stretch",placeholder='neha')

    teacher_password = st.text_input("Enter password",width="stretch",type='password',placeholder='password')

    st.divider()

    col1,col2 = st.columns(2)

    with col1:
        if st.button("Login",icon=':material/passkey:',icon_position='left',width='stretch',type='secondary'):
            if login_teacher(teacher_username,teacher_password):
                st.toast("Welcome back",icon="✌️")
                import time 
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username and password")
    with col2:
        if st.button("Register Instead",icon=':material/passkey:',icon_position='left',width='stretch',type='primary'):
            st.session_state.teacher_login_type='register'
            st.rerun()

    dashboard_footer()


def teacher_screen_register():

    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go to Home",shortcut='control+backspace',type='secondary',key='loginbckbtn'):
            st.session_state['login_type']=None
            st.rerun()

    st.header("Register with your teacher profile",text_alignment='center')
    
    st.space()
    
    teacher_username = st.text_input("Enter username",width="stretch",placeholder='neha')

    teacher_name = st.text_input("Enter Name",width="stretch",placeholder='Neha')

    teacher_password = st.text_input("Enter password",width="stretch",type='password',placeholder='password')

    teacher_pass_confim = st.text_input("Confirm password",width="stretch",type='password',placeholder='Re-enter password')

    st.divider()

    col1,col2 = st.columns(2)

    with col1:
        if st.button("Register now",width='stretch',type='primary'):
            success,message = teacher_register(teacher_username,teacher_name,teacher_password,teacher_pass_confim)
            if success:
                st.success(message)
                import time 
                time.sleep(2)
                st.session_state.teacher_login_type ='login'
                st.rerun()
            else:
                st.error(message)

    with col2:
        if st.button("Login Instead",width='stretch',type='secondary',shortcut='control+enter'):
            st.session_state.teacher_login_type = 'login'
            st.rerun()