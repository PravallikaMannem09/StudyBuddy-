from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

def generate_summary(vector_db):

    retriever = vector_db.as_retriever(search_kwargs={"k": 5})
    docs = retriever.invoke("summarize this content")

    text = "\n".join([d.page_content for d in docs])

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3,
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

    prompt = f"""
    Summarize this study material in bullet points:

    {text}
    """

    return llm.invoke(prompt).content