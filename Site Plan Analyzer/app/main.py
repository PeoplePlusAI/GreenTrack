import streamlit as st
from PIL import Image
import pytesseract

st.set_page_config(
    page_title="Site Plan Analyzer",
    page_icon="./static/favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Site Plan Analyzer")
st.write("Upload an Image file containing your site plan.")

uploaded_file = st.file_uploader("Upload a file", type=["jpg", "jpeg", "png"], accept_multiple_files=False, label_visibility='hidden')

if uploaded_file is not None:
    file_type = uploaded_file.type
    if file_type in ["image/jpeg", "image/png", "image/jpg"]:
        col1, col2 = st.columns([0.5, 0.5])

        image = Image.open(uploaded_file)
        string = pytesseract.image_to_string(image)

        with col1:
            st.image(image, use_column_width=True)

        with col2:
            st.markdown("### Parsed Text")
            st.write(string)
    else:
        st.write("Unsupported file format.")
