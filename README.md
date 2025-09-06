# 📄 RAG Application with ChromaDB & Gemini

This project implements a **Retrieval-Augmented Generation (RAG)** pipeline using **ChromaDB**, **Sentence Transformers**, and **Google Gemini**.
It allows you to upload **PDF** or **DOCX** documents, store their embeddings in ChromaDB, and query them using Gemini for intelligent question-answering.
The frontend is built with **Streamlit** for an interactive user experience.

---

## 🚀 Features

* 📤 Upload and process **PDF/DOCX** files.
* 🔎 Extract text automatically from documents.
* ✂️ Split text into chunks for efficient embedding & retrieval.
* 💾 Store embeddings persistently in **ChromaDB**.
* 🧠 Use **SentenceTransformers (MiniLM)** for embeddings.
* 🤖 Query documents with **Gemini LLM** to get contextual answers.
* 🧹 Clear stored embeddings anytime.
* 🎨 Simple and interactive **Streamlit UI**.

---

## 📂 Project Structure

```
├── main.py                 # Core logic (text extraction, chunking, embeddings, RAG query)
├── app.py                  # Streamlit frontend
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── chroma_db/              # Persistent ChromaDB storage
```

---

## ⚙️ Installation & Setup

1. **Clone the repository**

   ```bash
   git clone 
   cd <your-repo-name>
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # For Linux/Mac
   venv\Scripts\activate      # For Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory and add your Gemini credentials:

   ```env
   GOOGLE_API_KEY=your_google_gemini_api_key
   ```

---

## ▶️ Running the Application

Start the **Streamlit app**:

```bash
streamlit run app.py
```

---

## 🖥️ Usage

1. Open the Streamlit UI in your browser (usually `http://localhost:8501`).
2. Upload **PDF/DOCX** files from the sidebar.
3. Click **Process Documents** → embeddings will be created & stored in ChromaDB.
4. Type your question in the input box.
5. Click **Get Answer** to receive a Gemini-generated response.
6. Use **Clear All Stored Embeddings** in the sidebar to reset the collection.

---

## 🛠️ Tech Stack

* **Python 3.9+**
* **PyPDF2** – PDF text extraction
* **python-docx** – DOCX text extraction
* **SentenceTransformers** – Embeddings (MiniLM)
* **ChromaDB** – Vector storage
* **Google Gemini API** – LLM for answering queries
* **LangChain** – Text chunking & orchestration
* **Streamlit** – Frontend interface

---

## 📌 Example Queries

* *"What is the candidate’s experience with Python?"*
* *"Summarize the key responsibilities mentioned in this document."*
* *"Does this resume mention cloud platforms like AWS or Azure?"*

---

## 🧹 Clearing the Database

You can clear stored embeddings anytime using:

* The **Clear All Stored Embeddings** button in the sidebar, or
* Programmatically:

  ```python
  from main import clear_collection
  clear_collection()
  ```

---

## ✅ Requirements

Dependencies are listed in **`requirements.txt`**. Install with:

```bash
pip install -r requirements.txt
```

---

## 📜 License

This project is licensed under the MIT License.
