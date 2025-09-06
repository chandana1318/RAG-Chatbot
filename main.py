import PyPDF2
from docx import Document
from dotenv import load_dotenv
from langchain_together import ChatTogether
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb
from pathlib import Path
from google import genai

# Load environment variables
load_dotenv()

persistence_directory = 'chroma_db'
chroma_client = chromadb.PersistentClient(path=persistence_directory)
collection_name = 'chroma_collection'
collection = chroma_client.get_or_create_collection(name=collection_name)

embedder = SentenceTransformer("all-MiniLM-L6-v2")

# --- Helper: Extract text from PDF ---
def read_pdf(file) -> str:
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {e}"

# --- Helper: Extract text from DOCX ---
def read_docx(file) -> str:
    try:
        doc = Document(file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text.strip()
    except Exception as e:
        return f"Error reading DOCX: {e}"

# --- Text Chunking ---
def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200):
    """Splits text into smaller chunks for processing."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_text(text)

# --- Create Chunks and Store Embeddings in ChromaDB ---
def store_embeddings(text,doc_id):
    """Generates and stores embeddings for text chunks in ChromaDB."""
    chunks = chunk_text(text)

    ids = [f"{doc_id}_{i}" for i in range(len(chunks))]
    try:
        existing = collection.get(where = {"doc_id": doc_id}) 
        if existing and len(existing['ids']) > 0: 
            print(f"Document with id {doc_id} already exists in the database.")
            return
    except:
        pass
    embeddings = embedder.encode(chunks).tolist()
    collection.add(documents=chunks,
                    embeddings=embeddings,
                    metadatas=[{"doc_id":doc_id}]*len(chunks), 
                    ids= ids)
    return f"Stored {len(chunks)} chunks in the database."

# --- Retrieves relevant chunks based on the user query and LLM generates the response ---
def rag_query(query: str) -> str:
    """Generates an answer using Gemini based on the user query and relevant document chunks."""
    query_embedding = embedder.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=5)
    context = results['documents'][0]
    #print("Retrieved from the chroma db",results)
    prompt = f"""You are a knowledge base assistant.Your task is to answer the question based on the provided context. If the answer is not contained within the context, please respond with "I don't know".Answer in detail based on the context and user query.
    ---
    ##Input:
    *Context:{context}*
    *Question:{query}*
    ---
    Response format: 
    Human-readable markdown format
    """
    client = genai.Client()

    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
)

    return response.text


# --- Clear ChromaDB Collection ---
def clear_collection():
    """Clears the ChromaDB collection."""
    global collection

    chroma_client.delete_collection(name=collection_name)
    collection = chroma_client.create_collection(name=collection_name)
    return "Collection cleared."











