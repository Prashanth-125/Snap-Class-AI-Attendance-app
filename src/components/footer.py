import streamlit as st 

def home_footer():

    st.markdown(f"""

                <div style='display:flex; flex-direction:column; align-items:center; justify-content:center; margin-top:10px;'>
                    <p style='text-align:center; font-weight:bold; color:white;'>Created with ❤️ by Prashanth</p>
                </div>

                """,unsafe_allow_html=True)

def footer_dashboard():

    st.markdown(f"""

                <div style='display:flex; flex-direction:column; align-items:center; justify-content:center; margin-top:10px;'>
                    <p style='text-align:center; font-weight:bold; color:black;'>Created with ❤️ by Prashanth</p>
                </div>

                """,unsafe_allow_html=True)
