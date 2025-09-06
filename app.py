import streamlit as st
from main import read_pdf, read_docx, store_embeddings,clear_collection,collection,rag_query
from pathlib import Path
import tempfile
import os

# Streamlit App
st.title("📄 RAG Application")
st.write("Upload your documents (PDF or DOCX) to store its embeddings in ChromaDB. Then, ask questions about the documents!")

# Sidebar for PDF/DOCX Uploader and Instructions
st.sidebar.title("📤 Upload Documents")
uploaded_files = st.sidebar.file_uploader("Choose a PDF or DOCX file", type=["pdf", "docx"],accept_multiple_files=True)

# Process and store embeddings when files are uploaded
if st.sidebar.button("Process Documents"):
    if uploaded_files:
        with st.spinner("Processing and storing embeddings..."):
            for uploaded_file in uploaded_files:
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name
                doc_id = Path(uploaded_file.name).stem
                if uploaded_file.type == "application/pdf":
                    text = read_pdf(tmp_path)
                else:
                    text = read_docx(tmp_path)
                store_embeddings(text, doc_id)
                os.remove(tmp_path)
        st.sidebar.success("Documents processed and embeddings stored!")
    else:
        st.sidebar.warning("⚠️ Please upload at least one PDF or DOCX file.")

# Action button for clearing embeddings
st.sidebar.divider()
st.sidebar.header("Actions")
if st.sidebar.button("Clear All Stored Embeddings"):
    with st.spinner("Clearing all stored embeddings..."):
        clear_collection()
    st.sidebar.success("All stored embeddings cleared!")
    st.rerun()

# Check if there are any documents in the collection
doc_count = collection.count()

# If documents exist, show the query input
if doc_count > 0:
    st.subheader("Ask a Question about your uploaded Documents")
    user_query = st.text_input("Enter your question here", placeholder="e.g., What is the candidate's experience with Python?")
    if st.button("Get Answer"):
        if user_query.strip():
            with st.spinner("Fetching answer..."):
                answer = rag_query(user_query)
            st.markdown("### 📝 Answer")
            st.write(answer)
        else:
            st.error("⚠️ Please enter a question.")

else:
    st.info("ℹ️ No documents uploaded yet. Please upload PDFs or DOCX files to store embeddings and enable querying.")
