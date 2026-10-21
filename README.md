# 📄 RAG-Based Chat with PDF

An AI-powered **Retrieval-Augmented Generation (RAG)** application that allows users to upload multiple PDF documents and ask questions about their content using **Google Gemini, LangChain, FAISS, and semantic search**.

The application retrieves the most relevant information from uploaded documents before generating an answer, helping keep responses grounded in the provided PDF content.

---

## 🚀 Overview

Reading and extracting information from large PDF documents can be time-consuming.

This project provides an interactive question-answering system where users can:

- Upload one or multiple PDF documents.
- Extract text from the documents.
- Split documents into smaller semantic chunks.
- Convert chunks into vector embeddings.
- Store embeddings in a FAISS vector database.
- Retrieve the most relevant document chunks for a question.
- Generate an answer using Google Gemini.
- View the source document and page associated with retrieved information.

The application is built as a complete RAG pipeline rather than simply sending the entire document directly to an LLM.

---

## 🎯 Objectives

- Build a practical Retrieval-Augmented Generation application.
- Implement semantic search over PDF documents.
- Use vector embeddings for document retrieval.
- Integrate FAISS as a local vector database.
- Use Google Gemini for embeddings and response generation.
- Provide source-aware answers based on retrieved document context.
- Prevent the LLM from relying on unrelated outside knowledge.
- Create an interactive interface using Streamlit.
- Support multiple PDF documents in a single session.

---

# 🏗️ RAG Architecture

```text
                         ┌─────────────────────┐
                         │     PDF Documents   │
                         │                     │
                         │  Multiple PDFs      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    PDF Extraction   │
                         │      PyPDF2         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Text Chunking    │
                         │ RecursiveCharacter  │
                         │     TextSplitter    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Gemini Embeddings  │
                         │                     │
                         │ semantic vectors   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    FAISS Vector     │
                         │       Store         │
                         └──────────┬──────────┘
                                    │
                              User Question
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Similarity Search  │
                         │       Top K = 5     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Retrieved PDF     │
                         │      Context        │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Google Gemini    │
                         │        LLM          │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Source-Aware Answer│
                         │                     │
                         │ Document + Page     │
                         └─────────────────────┘
```

---

# 🔄 How the RAG Pipeline Works

## 1. PDF Upload

Users can upload multiple PDF documents through the Streamlit interface.

The application processes each document page by page.

Document metadata such as:

```text
Source filename
Page number
```

is preserved during processing.

---

## 2. Text Extraction

PDF text is extracted using **PyPDF2**.

Each page is converted into a LangChain `Document` object along with metadata identifying the original PDF and page.

This allows retrieved information to be traced back to its source.

---

## 3. Text Chunking

Large documents are divided into smaller chunks using:

**RecursiveCharacterTextSplitter**

Configuration:

```text
Chunk size: 1000
Chunk overlap: 150
```

Chunking makes the document content easier to embed and improves retrieval efficiency.

---

## 4. Vector Embeddings

Each text chunk is converted into a numerical vector using Google's Gemini embedding model:

```text
models/gemini-embedding-001
```

The embeddings represent the semantic meaning of the text.

This allows the application to search for information based on meaning rather than exact keyword matching.

---

## 5. FAISS Vector Store

The generated embeddings are stored in a **FAISS vector database**.

FAISS enables efficient similarity search over the document embeddings.

When a user asks a question, the question is compared against the stored vectors to identify the most relevant document chunks.

---

## 6. Semantic Retrieval

The application performs similarity search using:

```text
Top K = 5
```

The five most relevant document chunks are retrieved and provided to the language model as context.

```text
User Question
      ↓
Embedding / Similarity Search
      ↓
Top 5 Relevant Chunks
      ↓
Retrieved Context
```

---

## 7. Response Generation

The retrieved context is passed to Google's Gemini language model.

The application uses:

```text
Model: gemini-3.6-flash
Temperature: 0.2
```

The relatively low temperature is used to encourage more consistent responses.

---

# 🧠 Grounded Generation

A key part of the application is the prompt used for response generation.

The model is instructed to:

- Answer using the retrieved PDF context.
- Avoid inventing information.
- Avoid relying on unrelated outside knowledge.
- State when the requested information is not available in the documents.
- Mention the relevant document/page when useful.

Conceptually:

```text
Question
   +
Retrieved PDF Context
   ↓
Grounded Prompt
   ↓
Gemini LLM
   ↓
Answer
```

This is the core principle of Retrieval-Augmented Generation.

---

# 📚 Source-Aware Answers

The application preserves document metadata during ingestion.

Therefore, retrieved information can be associated with:

```text
Document
Page
```

This improves traceability and allows users to understand where the answer originated.

Example:

```text
Answer:
The document describes ...

Source:
example.pdf
Page: 12
```

---

# 🖥️ Application Interface

The application is built using **Streamlit**.

The interface provides:

### Document Upload

Upload one or multiple PDF files.

### Document Processing

The application extracts, chunks, embeds, and indexes the uploaded documents.

### Question Answering

Users can ask natural-language questions about the uploaded documents.

### Retrieved Sources

Relevant document chunks and their source information can be displayed alongside the generated answer.

---

# 🛠️ Technology Stack

## Programming

- Python

## Generative AI

- Google Gemini
- Gemini Embeddings
- Large Language Models
- Prompt Engineering

## RAG

- Retrieval-Augmented Generation
- Semantic Search
- Vector Embeddings
- Context Retrieval

## Frameworks & Libraries

- LangChain
- LangChain Core
- LangChain Text Splitters
- LangChain Google GenAI
- FAISS
- PyPDF2
- python-dotenv

## Frontend

- Streamlit

## Version Control

- Git
- GitHub

---



# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Vijaysinh-Bhosale/RAG-based-Chat-with-PDF.git
```

```bash
cd RAG-based-Chat-with-PDF
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Configuration

The application requires a Google API key for Gemini.

Create a `.env` file in the project root:

```text
GOOGLE_API_KEY=your_google_api_key
```

The `.env` file is intentionally excluded from Git using `.gitignore`.

**Never commit API keys or other credentials to GitHub.**

---

# ▶️ Run the Application

Start Streamlit from the project root:

```bash
streamlit run app.py
```

The application will open in your browser.

---

# 💻 Example Workflow

```text
1. Launch application
        ↓
2. Upload PDF documents
        ↓
3. Extract PDF text
        ↓
4. Split text into chunks
        ↓
5. Generate Gemini embeddings
        ↓
6. Build FAISS vector index
        ↓
7. Enter a question
        ↓
8. Retrieve top 5 relevant chunks
        ↓
9. Send retrieved context to Gemini
        ↓
10. Generate grounded answer
        ↓
11. Display answer + source information
```

---

# 🔍 Example Use Cases

The system can be used for document-based question answering such as:

- Research papers
- Technical documentation
- Business reports
- Academic notes
- Product documentation
- Policy documents
- Manuals
- Project documentation
- Multiple-document knowledge bases

---

# 🧩 Key Engineering Concepts Demonstrated

## Retrieval-Augmented Generation

Combines information retrieval with LLM generation so that responses are based on retrieved external context.

## Semantic Search

Retrieves information based on semantic similarity rather than simple keyword matching.

## Vector Embeddings

Represents document chunks as numerical vectors that capture semantic meaning.

## Vector Database

FAISS is used to efficiently search the embedding space.

## Prompt Engineering

The LLM prompt explicitly constrains the model to use retrieved document context.

## Source Traceability

Document and page metadata are preserved during ingestion to improve answer traceability.

---

# ⚠️ Limitations

This project is designed as a portfolio and demonstration application.

Current limitations include:

- PDF text extraction quality depends on the structure of the PDF.
- Scanned/image-only PDFs may require OCR.
- Retrieval quality depends on chunking and embedding quality.
- The system currently uses a fixed top-K retrieval value of 5.
- Large document collections may require a production-grade vector database.
- API usage is subject to Google Gemini availability and usage limits.
- The application does not currently implement a production authentication system.
- The local FAISS index is not committed to the repository.

---




# 🔐 Security Considerations

The project uses environment variables for API credentials.

Sensitive files are excluded through `.gitignore`:

```text
.env
.env.*
```

Local development artifacts are also excluded:

```text
venv/
faiss_index/
.vscode/
```

API credentials should never be hard-coded into the source code or committed to version control.

---

# 👨‍💻 Author

**Vijaysinh Yuvarj Bhosale**

Computer Engineering | Machine Learning | Generative AI | Python | SQL

### GitHub

https://github.com/Vijaysinh-Bhosale

---

# 📄 License

Copyright © 2026 Vijaysinh Yuvarj Bhosale.

