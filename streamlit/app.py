import requests
import streamlit as st
from streamlit_lottie import st_lottie

# ---- CONSTANTS ----
LOTTIE_URL = "https://lottie.host/2011bba0-0444-4c05-92e2-9e1ec63fef08/2CGPse9h3m.json"
STREAMLIT_URL = "https://www.streamlit.io"
CSS_FILE = "style/style.css"

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Basic Webpage", layout="wide")

# ---- FUNCTION TO LOAD LOTTIE JSON DATA ----
def load_lottieurl(url):
    """Loads lottie JSON data from a given URL."""
    try:
        r = requests.get(url)
        r.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        return r.json()
    except requests.RequestException as e:
        st.error(f"Failed to load Lottie URL: {str(e)}")
        return None

# ---- FUNCTION TO INSERT A LOCAL CSS FILE ----
def local_css(file_name):
    """Loads local CSS file into the app."""
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---- LOAD THE LOCAL CSS FILE ----
local_css(CSS_FILE)

# ---- LOAD THE LOTTIE ASSET ----
lottie_coding = load_lottieurl(LOTTIE_URL)

# ---- HEADER SECTION ----
with st.container():
    st.subheader("This is a basic Streamlit webpage")
    st.title("This is to demonstrate Streamlit")
    st.write("Streamlit is an open-source Python library designed to help developers "
             "create interactive and aesthetically pleasing web applications for data science "
             "and machine learning projects with minimal effort.")
    st.markdown(f"[Learn More >]({STREAMLIT_URL})", unsafe_allow_html=True)

# ---- COLUMN SECTION ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    
    with left_column:
        st.header("Left column header")
        st.write("""
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
            """)
    
    with right_column:
        if lottie_coding:
            st_lottie(lottie_coding, height=300, key="coding")
