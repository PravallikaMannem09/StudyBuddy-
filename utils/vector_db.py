from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")


def create_vector_db(pdf_path):

    # Load PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    # # Create embeddings
    from langchain_community.embeddings import HuggingFaceEmbeddings

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    # embeddings = GoogleGenerativeAIEmbeddings(
    #     model="gemini-embedding-001",
    #     google_api_key=GOOGLE_API_KEY
    # )

    # Create FAISS Vector Store
    vector_db = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    return vector_db