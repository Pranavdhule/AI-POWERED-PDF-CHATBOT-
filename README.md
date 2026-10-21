# 📄 AI-Powered PDF Chatbot

An AI-powered document question-answering application built using **Retrieval-Augmented Generation (RAG)**, Google Gemini, LangChain, FAISS, and Streamlit. Upload one or multiple PDF documents and ask questions in natural language to receive answers based on the information contained in your documents.

## 🚀 Project Overview

Reading lengthy PDFs, research papers, technical documents, and business reports can be time-consuming. This project simplifies document analysis by allowing users to upload PDFs and interact with their content through an AI-powered chatbot.

The application retrieves relevant text from uploaded documents and provides it to a language model to generate context-based answers.

## ✨ Key Features

- 📂 **Multiple PDF Uploads:** Upload multiple PDF documents in one session.
- 🧠 **AI-Powered Question Answering:** Ask questions in natural language.
- 🔍 **Semantic Search:** Retrieve relevant information based on meaning.
- ⚡ **FAISS Vector Database:** Efficient similarity search over document embeddings.
- 📑 **Page-Level Metadata:** Preserve source filenames and page numbers during document processing.
- 🛡️ **Context-Grounded Responses:** Instruct the language model to answer using retrieved document content.
- 📊 **Document Processing Status:** View processed documents, text chunks, and processing time.
- 🖥️ **Interactive Interface:** Use a simple interface developed with Streamlit.

## 🏗️ System Architecture

The application follows a Retrieval-Augmented Generation (RAG) pipeline.

```text
        Upload PDF Documents
                 |
                 v
          Extract PDF Text
                 |
                 v
          Split into Chunks
                 |
                 v
        Generate Embeddings
                 |
                 v
         FAISS Vector Store
                 |
                 v
          User's Question
                 |
                 v
         Semantic Retrieval
                 |
                 v
       Retrieve Relevant Text
                 |
                 v
       Google Gemini LLM
                 |
                 v
          Generated Answer
```

## 🔄 How It Works

1. **PDF Upload:** Users upload one or multiple PDF files through Streamlit.
2. **Text Extraction:** PyPDF2 extracts readable text from each PDF page.
3. **Text Chunking:** LangChain's `RecursiveCharacterTextSplitter` divides text into manageable chunks.
4. **Embedding Generation:** Google's Gemini embedding model converts text chunks into vector representations.
5. **Vector Storage:** FAISS stores the vectors for similarity search.
6. **Question Retrieval:** The application retrieves the five most relevant document chunks for a user's question.
7. **Answer Generation:** Google Gemini generates an answer using the retrieved document context.
8. **Response Display:** The application displays the answer and supports source-aware retrieval using document metadata.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| LangChain | RAG pipeline and document processing |
| Google Gemini | AI-powered answer generation |
| Gemini Embeddings | Semantic vector representations |
| FAISS | Vector similarity search |
| PyPDF2 | PDF text extraction |
| python-dotenv | Environment variable management |
| Git and GitHub | Version control and project hosting |

## 📁 Project Structure

```text
AI-POWERED-PDF-CHATBOT/
│
├── app.py
│   └── Main Streamlit application
│
├── requirements.txt
│   └── Python dependencies
│
├── README.md
│   └── Project documentation
│
└── .gitignore
    └── Files excluded from version control
```

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or a compatible version supported by the installed dependencies
- Git
- A Google Gemini API key
- An internet connection for API access

### 1. Clone the Repository

```bash
git clone https://github.com/Pranavdhule/AI-POWERED-PDF-CHATBOT-.git
```

### 2. Navigate to the Project Directory

```bash
cd AI-POWERED-PDF-CHATBOT-
```

### 3. Create a Virtual Environment

On Windows:

```powershell
python -m venv venv
```

Activate the environment:

```powershell
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure the Google Gemini API Key

Obtain an API key from [Google AI Studio](https://aistudio.google.com/).

Create a file named `.env` in the project root directory:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

Replace the placeholder with your own API key.

**Security note:** Never upload your `.env` file or expose your API key in source code, screenshots, or public repositories.

### 6. Run the Application

```bash
streamlit run app.py
```

Streamlit will provide a local URL, usually:

```text
http://localhost:8501
```

Open the URL in your browser.

## 💬 How to Use the Application

1. Launch the application.
2. Upload one or multiple PDF documents from the sidebar.
3. Click **Process Documents**.
4. Wait for text extraction, chunking, embedding generation, and vector indexing to finish.
5. Enter your question in the question field.
6. Click **Ask Question**.
7. Read the AI-generated response based on the retrieved document content.

### Example Questions

- What is the main objective of this document?
- Summarize the key findings of this research paper.
- What are the major challenges discussed in the report?
- Explain the methodology described in the PDF.
- Which page discusses a particular topic?

The quality of the answers depends on the readability of the PDFs, the available document content, and the relevance of retrieved text.

## 🎯 Use Cases

- Research paper analysis
- Academic study and revision
- Technical documentation search
- Business report analysis
- Policy and procedure review
- Product documentation assistance
- Information retrieval from lengthy PDF files

## 🔐 Security and Limitations

- A valid Google Gemini API key is required.
- API usage may incur charges or be subject to account quotas.
- Scanned PDFs without an embedded text layer may require OCR, which is not implemented in the current extraction pipeline.
- The model may occasionally produce inaccurate or incomplete answers.
- Answers should be verified against the original documents for important decisions.
- Uploaded documents are processed by the application and relevant text is sent to the configured Google AI service for embedding and answer generation.
- API keys and confidential documents should be handled securely.

## 🔮 Future Enhancements

- Chat history and conversational memory
- Support for Word documents and other file formats
- OCR for scanned PDFs
- Improved source citations and page references in answers
- Persistent vector database storage
- Advanced retrieval and reranking
- User authentication and access control
- Deployment to a cloud hosting platform

## 👨‍💻 Author

**Pranav Dhule**

GitHub: [@Pranavdhule](https://github.com/Pranavdhule)

Project Repository: [AI-POWERED-PDF-CHATBOT](https://github.com/Pranavdhule/AI-POWERED-PDF-CHATBOT-)

## 📜 License

This project is available for educational and personal portfolio purposes. Add an appropriate open-source license file if you intend to distribute it under a specific license.

---

⭐ If you find this project useful, consider giving the repository a star on GitHub.
