import streamlit as st


with st.container(border=True):
    col1, col2 = st.columns([1, 17])
    with col1:
        col1.image("./resources/images/deployed_code_24dp_EA3323_FILL0_wght400_GRAD0_opsz48.png")
    with col2:
        col2.subheader('Deploy to Cloudera AI Inference', divider='red')
        st.caption("Deploy your models to Cloudera AI Inference for production use and real-world application deployment.")

st.write("\n")
st.info("This Feature is coming soon !", icon=":material/info:")
