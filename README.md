# RAG Document Assistant

A production-ready **Retrieval-Augmented Generation (RAG)** system that allows users to upload documents (PDF, TXT, DOCX) and ask intelligent questions with accurate source citations.

Built using **FastAPI**, **FAISS**, **HuggingFace Embeddings**, and LLM integration (**Google Gemini** or **Ollama**).

---

## Overview

This project implements a complete RAG pipeline:

- Document ingestion and chunking  
- Vector embedding generation  
- FAISS vector storage  
- Semantic retrieval  
- LLM-powered answer generation  
- Source citation display  

The system ensures grounded answers strictly based on uploaded documents.

---

## Architecture

```
User
→ FastAPI Backend
→ Document Ingestion
→ Text Splitter
→ Embeddings
→ FAISS Vector Store
→ Semantic Retriever
→ LLM (Gemini or Ollama)
→ Answer with Sources
```

---

## Tech Stack

**Backend:** FastAPI  
**Vector Database:** FAISS  
**Embeddings:** sentence-transformers (all-MiniLM-L6-v2)  

**LLM Support:**
- Google Gemini API  
- Ollama (Local models such as llama3.1:8b)

**Frontend:** Gradio  
**Evaluation:** Custom evaluation pipeline  

---

## Features

- Upload PDF / TXT / DOCX documents  
- Semantic similarity search  
- Configurable score threshold  
- LLM grounded answer generation  
- Source citation display  
- Gemini or local LLM support  
- Modular clean architecture  
- Evaluation pipeline included  

---

## Project Structure

```
app/
 ├── api/            # FastAPI routes
 ├── ingestion/      # Document loading and splitting
 ├── retrieval/      # Semantic retriever
 ├── vectorstore/    # FAISS storage
 ├── llm/            # LLM pipeline and prompts
 ├── memory/         # Conversation memory
 ├── evaluation/     # Evaluation logic
 ├── security/       # Authentication (optional)
 └── main.py         # Application entry point

data/
 ├── documents/
 └── vectorstore/

ui/
 └── gradio_app.py
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/rag-document-assistant.git
cd rag-document-assistant
```

### Create virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

### For Gemini

```
GOOGLE_API_KEY=your_api_key_here
LLM_PROVIDER=gemini
```

### For Ollama

```
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.1:8b
```

---

## ▶ Running the System

### If using Ollama (local model)

```bash
ollama run llama3.1:8b
```

### Start backend

```bash
uvicorn app.main:app --reload
```

### Start frontend

```bash
python ui/gradio_app.py
```

Open in browser:

```
http://localhost:7860
```

---

## Example Questions

- What is a rational agent?  
- What is the main topic of this document?  
- Who are the authors?  
- What are the key findings?  
- Explain the self-attention mechanism.  

---

## Evaluation

The project includes an evaluation pipeline that:

- Generates synthetic Q&A pairs  
- Measures retrieval quality  
- Evaluates grounding accuracy  

Run:

```bash
python app/scripts/run_evaluation.py
```

---

## How It Works

1. Documents are split into chunks.  
2. Each chunk is converted into embeddings.  
3. FAISS stores vectors for similarity search.  
4. The user question is embedded.  
5. Top-k similar chunks are retrieved.  
6. The LLM generates an answer using retrieved context only.  
7. Sources are displayed with page references.  

---

## Future Improvements

- Hybrid Search (BM25 + Vector Search)  
- Multi-document memory  
- Streaming responses  
- Docker deployment  
- Cloud deployment  
- Admin dashboard  

---

## Author

**Mohamed Dyaa**  
