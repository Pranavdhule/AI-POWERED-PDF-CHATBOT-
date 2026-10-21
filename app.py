import os
import time
import streamlit as st

from dotenv import load_dotenv
from PyPDF2 import PdfReader

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI,
)
from langchain_community.vectorstores import FAISS


# =========================================================
# CONFIGURATION
# =========================================================

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error(
        "GOOGLE_API_KEY not found. "
        "Please add it to your .env file."
    )
    st.stop()


st.set_page_config(
    page_title="AI PDF Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>
        .main-title {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            font-size: 1.05rem;
            opacity: 0.75;
            margin-bottom: 2rem;
        }

        .source-box {
            padding: 12px;
            border-radius: 8px;
            border: 1px solid rgba(128,128,128,0.25);
            margin-bottom: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "processed_files" not in st.session_state:
    st.session_state.processed_files = []

if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0

if "processing_time" not in st.session_state:
    st.session_state.processing_time = 0


# =========================================================
# LOAD GEMINI EMBEDDING MODEL
# =========================================================

@st.cache_resource
def get_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY,
    )


# =========================================================
# LOAD GEMINI CHAT MODEL
# =========================================================

@st.cache_resource
def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0.2,
        google_api_key=GOOGLE_API_KEY,
    )


# =========================================================
# EXTRACT PDF CONTENT
# =========================================================

def extract_pdf_documents(pdf_files):

    documents = []

    for pdf_file in pdf_files:

        try:
            reader = PdfReader(pdf_file)

            for page_number, page in enumerate(reader.pages, start=1):

                text = page.extract_text()

                if text and text.strip():

                    document = Document(
                        page_content=text.strip(),
                        metadata={
                            "source": pdf_file.name,
                            "page": page_number,
                        },
                    )

                    documents.append(document)

        except Exception as e:

            st.warning(
                f"Could not read {pdf_file.name}: {str(e)}"
            )

    return documents


# =========================================================
# SPLIT DOCUMENTS INTO CHUNKS
# =========================================================

def create_chunks(documents):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len,
    )

    chunks = text_splitter.split_documents(documents)

    return chunks


# =========================================================
# CREATE FAISS VECTOR STORE
# =========================================================

def create_vector_store(chunks):

    embeddings = get_embeddings()

    vector_store = FAISS.from_documents(
        chunks,
        embedding=embeddings,
    )

    return vector_store


# =========================================================
# EXTRACT TEXT FROM GEMINI RESPONSE
# =========================================================

def extract_response_text(response):

    content = response.content

    # Normal string response
    if isinstance(content, str):
        return content

    # Structured Gemini response
    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, str):
                text_parts.append(item)

            elif isinstance(item, dict):

                if item.get("type") == "text":
                    text_parts.append(
                        item.get("text", "")
                    )

        return "\n".join(text_parts).strip()

    return str(content)


# =========================================================
# ANSWER QUESTION
# =========================================================

def answer_question(question):

    vector_store = st.session_state.vector_store

    if vector_store is None:
        return None, []

    # Retrieve relevant chunks
    documents = vector_store.similarity_search(
        question,
        k=5,
    )

    if not documents:
        return None, []

    # Build context
    context_parts = []

    for i, document in enumerate(documents, start=1):

        source = document.metadata.get(
            "source",
            "Unknown document",
        )

        page = document.metadata.get(
            "page",
            "Unknown",
        )

        context_parts.append(
            f"""
SOURCE {i}
Document: {source}
Page: {page}

Content:
{document.page_content}
"""
        )

    context = "\n".join(context_parts)

    # Prompt
    prompt = f"""
You are an intelligent PDF question-answering assistant.

Answer the user's question using ONLY the information
provided in the retrieved PDF context.

Rules:

1. Do not invent information.
2. Do not use outside knowledge.
3. If the answer cannot be found in the context,
   say that the information is not available in the
   provided documents.
4. Give a clear and concise answer.
5. When useful, mention the relevant document and page.
6. Do not expose internal metadata, signatures,
   system information, or retrieval details.

Retrieved PDF Context:

{context}

User Question:

{question}

Answer:
"""

    llm = get_llm()

    response = llm.invoke(prompt)

    answer = extract_response_text(response)

    return answer, documents


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">📄 AI PDF Assistant</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Upload your documents and ask questions using "
    "AI-powered semantic search."
    "</div>",
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("📂 Document Manager")

    pdf_files = st.file_uploader(
        "Upload PDF documents",
        type=["pdf"],
        accept_multiple_files=True,
        help="You can upload multiple PDF files.",
    )

    st.divider()

    process_button = st.button(
        "⚡ Process Documents",
        use_container_width=True,
        type="primary",
    )

    if process_button:

        if not pdf_files:

            st.warning(
                "Please upload at least one PDF document."
            )

        else:

            start_time = time.time()

            with st.status(
                "Processing documents...",
                expanded=True,
            ) as status:

                # -----------------------------------------
                # Step 1
                # -----------------------------------------

                status.write(
                    "📄 Extracting text from PDFs..."
                )

                documents = extract_pdf_documents(
                    pdf_files
                )

                if not documents:

                    status.update(
                        label="No readable text found.",
                        state="error",
                    )

                    st.stop()

                # -----------------------------------------
                # Step 2
                # -----------------------------------------

                status.write(
                    "✂️ Splitting documents into chunks..."
                )

                chunks = create_chunks(
                    documents
                )

                # -----------------------------------------
                # Step 3
                # -----------------------------------------

                status.write(
                    "🧠 Creating semantic embeddings..."
                )

                vector_store = create_vector_store(
                    chunks
                )

                # -----------------------------------------
                # Save state
                # -----------------------------------------

                st.session_state.vector_store = (
                    vector_store
                )

                st.session_state.processed_files = [
                    pdf.name
                    for pdf in pdf_files
                ]

                st.session_state.chunk_count = (
                    len(chunks)
                )

                st.session_state.processing_time = (
                    time.time() - start_time
                )

                status.update(
                    label="Documents processed successfully!",
                    state="complete",
                )

            st.success("✅ Ready to chat!")


# =========================================================
# DOCUMENT STATUS
# =========================================================

if st.session_state.vector_store is not None:

    st.subheader("📊 Document Status")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "PDFs",
            len(
                st.session_state.processed_files
            ),
        )

    with col2:
        st.metric(
            "Text Chunks",
            st.session_state.chunk_count,
        )

    with col3:
        st.metric(
            "Processing Time",
            f"{st.session_state.processing_time:.1f}s",
        )

    with st.expander("📁 Processed Documents"):

        for filename in st.session_state.processed_files:
            st.write(f"• {filename}")


# =========================================================
# QUESTION AREA
# =========================================================

st.divider()

st.subheader("💬 Ask a Question")

question = st.text_input(
    "Question",
    placeholder="e.g. What is the core idea of the project?",
    label_visibility="collapsed",
)


# =========================================================
# ASK BUTTON
# =========================================================

if st.button(
    "🔎 Ask Question",
    type="primary",
):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    elif st.session_state.vector_store is None:

        st.warning(
            "Please upload and process a PDF first."
        )

    else:

        with st.spinner(
            "Searching documents and generating answer..."
        ):

            try:

                answer, source_documents = (
                    answer_question(question)
                )

                if answer:

                    st.subheader("🤖 Answer")

                    st.write(answer)

                    # -------------------------------------
                    # Sources
                    # -------------------------------------

                    if source_documents:

                        st.subheader("📚 Sources")

                        displayed_sources = set()

                        for document in source_documents:

                            source = document.metadata.get(
                                "source",
                                "Unknown",
                            )

                            page = document.metadata.get(
                                "page",
                                "Unknown",
                            )

                            source_key = (
                                source,
                                page,
                            )

                            if source_key not in displayed_sources:

                                displayed_sources.add(
                                    source_key
                                )

                                st.markdown(
                                    f"""
                                    <div class="source-box">
                                    📄 <b>{source}</b>
                                    &nbsp; — &nbsp;
                                    Page <b>{page}</b>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                else:

                    st.info(
                        "I couldn't find enough relevant "
                        "information in the uploaded documents."
                    )

            except Exception as e:

                st.error(
                    "An error occurred while generating "
                    "the answer."
                )

                st.exception(e)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "AI PDF Assistant • "
    "Streamlit • LangChain • Gemini • FAISS"
)