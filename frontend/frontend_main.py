import streamlit as st
import requests
import uuid

# st.set_page_config(page_title="DocTalk - Chat with Documents", layout="wide")
# st.markdown("<h1 style='text-align: center; color: #FF5733;'>📄 DocTalk — Chat with Your Documents</h1>", unsafe_allow_html=True)

# # === Sidebar ===
# with st.sidebar:
#     st.header("📤 Upload Documents")
#     uploaded_files = st.file_uploader("Choose files", type=["txt", "docx", "pdf"], accept_multiple_files=True)

#     if uploaded_files:
#         if len(uploaded_files) > 20:
#             st.error("You can only upload up to 20 files.")
#         else:
#             if st.button("Upload"):
#                 files = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
#                 with st.spinner("Uploading and processing..."):
#                     response = requests.post("http://localhost:8000/upload/", files=files)
#                 if response.ok:
#                     st.success("✅ Files uploaded successfully!")
#                     try:
#                         result = response.json()
#                         if isinstance(result, (dict, list)):
#                             st.json(result)
#                         else:
#                             st.warning("⚠️ Non-JSON object:")
#                             st.code(result)
#                     except Exception:
#                         st.error("❌ Upload failed.")
#                         st.write(response.text)

# # === Session State Init ===
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "input_key" not in st.session_state:
#     st.session_state.input_key = str(uuid.uuid4())  # Unique key to force refresh input

# # === Query Handler ===
# def handle_user_query(query, spinner_placeholder):
#     spinner_placeholder.markdown("⏳ Thinking...")
#     try:
#         response = requests.post("http://localhost:8000/hackrx/run/", json={"query": query})
#         if response.ok:
#             answer = response.json().get("response", "No response.")
#             st.session_state.chat_history.append((query, answer))
#         else:
#             st.session_state.chat_history.append((query, f"❌ Error: {response.text}"))
#     except Exception as e:
#         st.session_state.chat_history.append((query, f"⚠️ Connection Error: {str(e)}"))
#     spinner_placeholder.empty()
#     # Trigger field reset by changing key
#     st.session_state.input_key = str(uuid.uuid4())

# # === Layout ===
# col1, col2 = st.columns([1, 3])
# with col2:
#     st.subheader("💬 Chat Window")

#     for q, a in st.session_state.chat_history:
#         st.markdown(f"<div style='background-color:#36454F;color:#fdfefe;padding:10px;border-radius:8px;margin-bottom:5px'><b>You:</b> {q}</div>", unsafe_allow_html=True)
#         st.markdown(f"<div style='background-color:#36454F;color:#fdfefe;padding:10px;border-radius:8px;margin-bottom:10px'><b>DocTalk:</b> {a}</div>", unsafe_allow_html=True)

#     st.markdown("---")

#     spinner_placeholder = st.empty()

#     with st.form("chat_form"):
#         query = st.text_input("Type your question below", key=st.session_state.input_key, placeholder="Enter your query")
#         submitted = st.form_submit_button("Ask")
#         if submitted and query.strip():
#             handle_user_query(query.strip(), spinner_placeholder)







# st.title("DocTalk - Chat with Documents")

# uploaded_files = st.file_uploader("Choose files", type=["txt", "docx", "pdf"], accept_multiple_files=True)

# if uploaded_files:
#     if len(uploaded_files) > 20:
#         st.error("You can only upload up to 20 files.")
#     else:
#         if st.button("Upload"):
#             files = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
#             response = requests.post("http://localhost:8000/upload/", files=files)
#             if response.ok:
#                 st.success("Files uploaded successfully")
#                 st.json(response.json())
#             else:
#                 st.error("Upload failed")


# query = st.text_input("Query with your document")

# if st.button("Ask") and query:
#     response = requests.post("http://localhost:8000/Ask/", json={"query": query})
#     if response.ok:
#         st.write(response.json()["response"])
#     else:
#         st.error("Failed to get response")
#         st.write(response.text)


import streamlit as st
import requests
import os

# API endpoint & token
API_URL = "http://localhost:8000/hackrx/run"
API_TOKEN = os.getenv("HACKER_RX_TOKEN")

st.title("📄 HackRx PDF QA")

# PDF URL input
pdf_url = st.text_input("Enter PDF URL", placeholder="https://example.com/file.pdf")

# Question input
questions = st.text_area(
    "Enter your questions (one per line)",
    placeholder="What is the main topic?\nList the key points."
)

if st.button("Run"):
    if not pdf_url or not questions.strip():
        st.warning("Please enter both PDF URL and at least one question.")
    else:
        question_list = [q.strip() for q in questions.split("\n") if q.strip()]

        try:
            with st.spinner("Processing..."):
                response = requests.post(
                    API_URL,
                    json={"pdf_url": pdf_url, "questions": question_list},
                    headers={"Authorization": f"Bearer {API_TOKEN}"}
                )

                if response.status_code == 200:
                    answers = response.json()
                    for i, ans in enumerate(answers, start=1):
                        st.markdown(f"**Q{i}:** {question_list[i-1]}")
                        st.write(ans)
                        st.markdown("---")
                else:
                    st.error(f"Error {response.status_code}: {response.text}")

        except Exception as e:
            st.error(f"Request failed: {str(e)}")




