from langchain_google_genai import ChatGoogleGenerativeAI

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = st.secrets.get(
    "GEMINI_API_KEY",
    os.getenv("GEMINI_API_KEY")
)

def generate_flashcards(vector_db):

    retriever = vector_db.as_retriever(search_kwargs={"k": 10})
    docs = retriever.invoke("key concepts")

    text = "\n".join([d.page_content for d in docs])

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.4,
        google_api_key=GEMINI_API_KEY
    )

    prompt = f"""
    Convert this into flashcards:

    Format:
    Front: Question
    Back: Answer

    Content:
    {text}
    """

    return llm.invoke(prompt).content