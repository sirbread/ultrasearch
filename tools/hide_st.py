import streamlit as st

def footer():
    ''' Hide the "made with Streamlit"
        footer.
    '''
    st.markdown("""
            <style>
            footer {visibility: hidden;}
            </style>
            """,
            unsafe_allow_html=True)

def header():
    ''' Hide the stream header.
    '''
    st.markdown("""
            <style>
            header {visibility: hidden;}
            </style>
            """,
            unsafe_allow_html=True)