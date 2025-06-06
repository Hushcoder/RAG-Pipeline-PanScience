import streamlit as st
import requests

st.title("Upload Documents")

uploaded_files = st.file_uploader("Choose files", type=["txt", "docx", "pdf"], accept_multiple_files=True)

if uploaded_files:
    if len(uploaded_files) > 20:
        st.error("You can only upload up to 20 files.")
    else:
        if st.button("Upload"):
            files = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
            response = requests.post("http://localhost:8000/upload/", files=files)
            if response.ok:
                st.success("Files uploaded successfully")
                st.json(response.json())
            else:
                st.error("Upload failed")
                st.write(response.text)


