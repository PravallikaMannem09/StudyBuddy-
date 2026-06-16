import streamlit as st
import tempfile

from utils.vector_db import create_vector_db
from utils.rag_chain import create_rag_chain, ask_question

from features.summary import generate_summary
from features.quiz_generator import generate_quiz
from features.flashcards import generate_flashcards


# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="StudyBuddy AI",
    page_icon="🧠",
    layout="wide"
)

# -------------------------
# HEADER
# -------------------------
st.title("🧠 StudyBuddy AI")
st.markdown("Your smart AI tutor for instant doubt solving + exam prep")


# -------------------------
# SIDEBAR SETTINGS
# -------------------------
st.sidebar.title("📚 Study Tools")

uploaded_file = st.sidebar.file_uploader(
    "Upload your notes (PDF)",
    type=["pdf"]
)

tool_mode = st.sidebar.selectbox(
    "Choose Mode",
    ["💬 Chat Tutor", "📝 Summary", "🧠 Quiz", "🧩 Flashcards"]
)


# -------------------------
# SESSION STATE
# -------------------------
if "vector_db" not in st.session_state:
    st.session_state.vector_db = None

if "chain" not in st.session_state:
    st.session_state.chain = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# -------------------------
# PROCESS PDF
# -------------------------
if uploaded_file:

    with st.spinner("Reading your notes... 📄"):

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            pdf_path = tmp_file.name

        vector_db = create_vector_db(pdf_path)

        st.session_state.vector_db = vector_db
        st.session_state.chain = create_rag_chain(vector_db)

        st.sidebar.success("Study material loaded ✅")


# -------------------------
# MAIN LOGIC
# -------------------------
if not st.session_state.vector_db:
    st.info("👈 Upload your PDF from sidebar to start using StudyBuddy")
    st.stop()


# ======================================================
# 1. CHAT MODE (MAIN FEATURE)
# ======================================================
if tool_mode == "💬 Chat Tutor":

    st.subheader("💬 Ask your doubts instantly")

    question = st.text_input("Type your question here")

    if st.button("Ask StudyBuddy"):

        if question.strip():

            with st.spinner("Thinking like your tutor... 🤔"):

                answer= ask_question(
                    st.session_state.chain,
                    question
                )

            # Save chat history
            st.session_state.chat_history.append((question, answer))

    # Display chat history
    st.markdown("### 🧾 Conversation")

    for q, a in reversed(st.session_state.chat_history):
        st.markdown(f"**🧑 You:** {q}")
        st.markdown(f"**🧠 StudyBuddy:** {a}")
        st.divider()


# ======================================================
# 2. SUMMARY MODE
# ======================================================
elif tool_mode == "📝 Summary":

    st.subheader("📝 Smart Notes Summary")

    if st.button("Generate Summary"):

        with st.spinner("Creating concise notes..."):

            summary = generate_summary(st.session_state.vector_db)

        st.success("Done!")
        st.write(summary)


# ======================================================
# 3. QUIZ MODE
# ======================================================
elif tool_mode == "🧠 Quiz":

    st.subheader("🧠 Practice MCQs")

    if st.button("Generate Quiz"):

        with st.spinner("Preparing exam questions..."):

            quiz = generate_quiz(st.session_state.vector_db)

        st.success("Quiz Ready!")
        st.write(quiz)


# ======================================================
# 4. FLASHCARDS MODE
# ======================================================
elif tool_mode == "🧩 Flashcards":

    st.subheader("🧩 Revision Flashcards")

    if st.button("Generate Flashcards"):

        with st.spinner("Building memory cards..."):

            flashcards = generate_flashcards(st.session_state.vector_db)

        st.success("Flashcards Ready!")
        st.write(flashcards)
