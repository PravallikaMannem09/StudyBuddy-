import streamlit as st
import tempfile

from utils.vector_db import create_vector_db
from utils.rag_chain import create_rag_chain, ask_question

st.set_page_config(
    page_title="StudyBuddy",
    page_icon="📚",
    layout="wide"
)

st.title("📚 StudyBuddy")
st.subheader("Chat with Your Notes and Learn Smarter")

if "chain" not in st.session_state:
    st.session_state.chain = None

uploaded_file = st.file_uploader(
    "Upload your PDF notes",
    type=["pdf"]
)

if uploaded_file:

    with st.spinner("Reading your notes..."):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as tmp_file:

            tmp_file.write(uploaded_file.read())
            pdf_path = tmp_file.name

        vector_db = create_vector_db(pdf_path)

        st.session_state.chain = create_rag_chain(
            vector_db
        )

        st.success("Notes uploaded successfully!")

if st.session_state.chain:

    st.subheader("Ask Anything From Your Notes")

    question = st.text_input(
        "Type your question here"
    )

    if st.button("Ask StudyBuddy"):

        if question:

            answer = ask_question(
                st.session_state.chain,
                question
            )

            st.subheader("Answer")
            st.write(answer)