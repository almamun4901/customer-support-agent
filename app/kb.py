from typing import List
import os

import chromadb
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

CHROMA_HOST = os.getenv("CHROMA_HOST", "chroma")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))
COLLECTION_NAME = "support_kb"

def _get_embeddings():
    """Use a local HuggingFace model for embeddings — no API key needed."""
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
    )

def _get_vectorstore():
    embeddings = _get_embeddings()

    client = chromadb.HttpClient(host="chroma", port=8000)

    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        client=client,
    )

def ingest_kb(file_path: str):
    """
    Run once to populate KB from markdown or txt file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
    )

    chunks = splitter.split_text(text)

    docs = [Document(page_content=c) for c in chunks]

    vs = _get_vectorstore()
    vs.add_documents(docs)

    print(f"Ingested {len(docs)} KB chunks.")

def retrieve_context(query: str, k: int = 4) -> str:
    """
    Retrieve relevant KB context for a query.
    """
    vs = _get_vectorstore()

    docs = vs.similarity_search(query, k=k)

    if not docs:
        return ""

    return "\n\n---\n\n".join(d.page_content for d in docs)
