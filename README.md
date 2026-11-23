# 🚀 NASA Report RAG – AI-Powered PDF Question Answering System

An intelligent **Retrieval-Augmented Generation (RAG)** application that allows users to ask questions about NASA reports and receive relevant answers directly from PDF documents.

Built using Python, Flask, LangChain, Vector Search and modern AI technologies.

---

## 🌟 Project Overview

NASA Report RAG is a PDF-based Question Answering System designed to make reading and understanding large documents easier.

Instead of manually searching through hundreds of pages, users can upload or access a PDF document, ask questions in natural language, and retrieve relevant information with page references.

The application uses a Retrieval-Augmented Generation (RAG) approach to find relevant document content before generating an answer.

**Demo Document:** `NASA_100_Page_Report_Siddhant_Kumar.pdf`

---

## ✨ Key Features

- 📄 **PDF Document Processing:** Extracts text from PDF documents.
- 🔍 **Intelligent Search:** Retrieves relevant information based on user queries.
- 🤖 **AI-Powered Question Answering:** Supports an optional OpenAI-compatible LLM.
- 📚 **Context-Based Responses:** Generates answers using retrieved document content.
- 📌 **Page References:** Provides page references to help users locate information.
- ⚡ **Local Extractive Answers:** Can provide extractive answers without an LLM API key.
- 🌐 **Web Interface:** Simple interface built using Flask, HTML, CSS and JavaScript.
- 🧪 **Testing Support:** Includes automated tests using Pytest.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| LangChain | RAG workflow and document processing |
| PyPDFLoader | PDF text extraction |
| RecursiveCharacterTextSplitter | Text chunking |
| FastEmbed | Text embeddings |
| Qdrant | Vector database and similarity search |
| OpenAI-compatible API | Optional LLM integration |
| HTML, CSS, JavaScript | Frontend development |
| Pytest | Application testing |

---

## 🏗️ Project Architecture

```text
             NASA PDF Document
                     |
                     ▼
               PDF Loader
                     |
                     ▼
             Text Extraction
                     |
                     ▼
               Text Splitting
                     |
                     ▼
              Text Embeddings
                     |
                     ▼
             Qdrant Vector Store
                     |
                     ▼
              User Question
                     |
                     ▼
             Similarity Search
                     |
                     ▼
             Relevant Context
                     |
                     ▼
              Answer Generation
                     |
                     ▼
              Final Answer
             + Page References
```

---

## 📂 Project Structure

```text
RAG-PROJECT/
│
├── static/
│   ├── app.js
│   └── style.css
│
├── templates/
│   └── index.html
│
├── app.py
├── main.py
├── requirements.txt
├── test_app.py
├── README.md
├── .env.example
└── .gitignore
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Siddhant-1436/RAG-Project.git
```

### 2. Navigate to the Project Directory

```bash
cd RAG-Project
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate Virtual Environment

**Windows:**

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables

Create a `.env` file in the root directory.

Use `.env.example` as a reference.

```env
PORT=5000
FLASK_DEBUG=0
LLM_API_KEY=
LLM_MODEL=gpt-4o-mini
OPENAI_BASE_URL=https://api.openai.com/v1
```

Add your own API key if you want to enable LLM-based answers.

**Important:** Never upload your actual `.env` file or API keys to GitHub.

### 7. Run the Application

```bash
python app.py
```

### 8. Open in Browser

```text
http://localhost:5000
```

---

## 🧪 Run Tests

Execute the following command:

```bash
pytest -q
```

This runs the available automated tests.

---

## 💡 How It Works

1. The application loads the NASA PDF document.
2. PDF content is extracted into text.
3. The extracted text is divided into smaller chunks.
4. Text chunks are converted into vector embeddings.
5. Embeddings are stored in a Qdrant vector database.
6. The user enters a question through the web interface.
7. The system retrieves relevant document chunks.
8. Relevant context is used to generate an answer.
9. The application displays the answer with page references.

---

## 🎯 Project Objectives

- Simplify information retrieval from large PDF documents.
- Reduce manual document searching.
- Understand practical implementation of RAG architecture.
- Explore vector databases and semantic search.
- Integrate AI-powered question answering into a web application.

---

## 🔮 Future Enhancements

- Support for multiple PDF documents.
- Chat history and conversation memory.
- Improved document retrieval and ranking.
- Support for additional file formats.
- Cloud deployment using AWS.
- Enhanced user interface and document management.

---

## 👨‍💻 Developer

**Siddhant Kumar**

B.Tech – Computer Science (Data Science & AI)

**Project:** NASA Report RAG – AI-Powered PDF Question Answering System

---

## 📌 Acknowledgements

- NASA for the reference report.
- LangChain for document processing and RAG components.
- Qdrant for vector search capabilities.
- Flask for backend web development.

---

⭐ If you find this project interesting, consider giving the repository a star!

**GitHub Repository:**  
https://github.com/Siddhant-1436/RAG-Project
