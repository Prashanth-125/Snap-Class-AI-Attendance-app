import streamlit as st 
import io 
import segno 

@st.dialog("Share Class Link")
def share_subject_dialog(sub_name,sub_code):

    app_domain = "snapclass-main14.streamlit.app"
    join_url = f"{app_domain}/?join-code={sub_code}"

    qr = segno.make(join_url)

    out = io.BytesIO()

    qr.save(out,kind='png',scale=10,border=1)

    st.header("Scan to Join")

    col1,col2 = st.columns(2)
    with col1:
        st.markdown('### Copy Link')
        st.code(join_url,language="text")
        st.code(sub_code,language="text")
        st.info("Share this code in Whatsapp or Email")

    with col2:
        st.markdown("### Scan to JOIN")
        st.image(out.getvalue(), caption='QRCODE for class joining')