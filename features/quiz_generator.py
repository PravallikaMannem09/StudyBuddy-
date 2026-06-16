from langchain_google_genai import ChatGoogleGenerativeAI

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = st.secrets.get(
    "GEMINI_API_KEY",
    os.getenv("GEMINI_API_KEY")
)
def generate_quiz(vector_db):

    retriever = vector_db.as_retriever(search_kwargs={"k": 10})
    docs = retriever.invoke("important questions")

    text = "\n".join([d.page_content for d in docs])

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.5,
        google_api_key=GEMINI_API_KEY
    )

    prompt = f"""
    Create 5 MCQs from this content:

    {text}

    Format:
    Q1:
    A)
    B)
    C)
    D)
    Answer:
    """

    return llm.invoke(prompt).content