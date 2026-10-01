# MarkWise AI

MarkWise AI is an AI-powered application that helps users analyze
information and interact with documents using artificial intelligence.

## 🚀 Smart Document Assistant

The project includes a Retrieval-Augmented Generation (RAG) based
Document Q&A system.

Users can upload one or more PDF or TXT documents and ask questions
about their content. The system retrieves the most relevant document
sections and provides them as context to an AI model before generating
the answer.

## ✨ Features

- 📄 Upload PDF and TXT documents
- 📝 Extract text from documents
- ✂️ Split documents into overlapping chunks
- 🧠 Generate semantic embeddings
- 🔎 Retrieve relevant document chunks
- 📊 Calculate cosine similarity
- 🤖 Generate grounded AI answers
- 📌 Display retrieved source context
- 📖 Display source document and page number
- 🛡️ Reduce hallucinations by grounding answers in retrieved context
- 📚 Support multiple uploaded documents

## 🧠 RAG Pipeline

The application follows this pipeline:

User Documents
      ↓
Text Extraction
      ↓
Text Chunking
      ↓
Embedding Generation
      ↓
Question Embedding
      ↓
Cosine Similarity Search
      ↓
Top Relevant Chunks
      ↓
LLM Context
      ↓
Grounded Answer

## 🔧 Technologies Used

- Python
- Flask
- HTML
- CSS
- PyMuPDF
- Sentence Transformers
- scikit-learn
- NumPy
- OpenRouter API
- Jinja2

## 🧠 Embedding Model

The application uses:

`all-MiniLM-L6-v2`

for generating semantic embeddings of document chunks and user
questions.

## 🔎 Retrieval

The question embedding is compared with document chunk embeddings
using cosine similarity.

The system retrieves the top relevant chunks and provides them to the
language model as context.

## 🤖 AI Generation

The retrieved document context is sent to the language model through
the OpenRouter API.

The model is instructed to:

1. Answer only using the retrieved document context.
2. Avoid using outside knowledge.
3. Avoid inventing information.
4. State when the requested information cannot be found.

## 📌 Source Transparency

For each retrieved section, the application displays:

- Source file name
- Page number
- Similarity score
- Retrieved text

This allows users to understand which document sections were used to
generate the answer.

## 🛡️ Hallucination Reduction

The system uses retrieved document context instead of directly asking
the language model to answer from its general knowledge.

If the required information is not available in the retrieved context,
the application instructs the model to state that the information could
not be found in the uploaded document.

## 📁 Project Structure

```text
MarkWise-AI/
│
├── templates/
│   ├── index.html
│   └── intermediate.html
│
├── app.py
├── .env
├── requirements.txt
├── Procfile
└── README.md

Live Demo
https://sandya05.pythonanywhere.com/?utm_source=chatgpt.com
