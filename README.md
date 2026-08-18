# 🎥 YouTube RAG Chatbot

An AI-powered **YouTube RAG (Retrieval-Augmented Generation) Chatbot** that allows users to ask questions about a YouTube video. The application extracts the video's transcript, splits it into chunks, generates embeddings, stores them in a FAISS vector store, retrieves relevant context, and uses **Google Gemini** to generate accurate, context-aware answers.
## 🎯 Project Objective
The main objective of this project is to understand and implement an end-to-end Generative AI RAG application, covering the complete workflow from data ingestion and embeddings to semantic retrieval, context augmentation, and LLM-based response generation.
## 🚀 Features

- 🎥 Enter a YouTube video URL
- 📝 Automatically extract the video transcript
- ✂️ Split transcript into smaller chunks
- 🔢 Generate embeddings using Google Gemini
- 🗄️ Store embeddings in FAISS vector store
- 🔍 Retrieve relevant transcript chunks using semantic search
- 🤖 Generate answers using Gemini 2.5 Flash
- 💬 Interactive Streamlit chatbot interface
- 📺 Watch the YouTube video while chatting
- 🧠 Retrieval-Augmented Generation (RAG) pipeline

## 🛠️ Tech Stack
- Python – Programming language
- Streamlit – Web application and chatbot UI
- LangChain – RAG pipeline and LLM orchestration
- Google Gemini – LLM and text embeddings
- FAISS – Vector store and similarity search
- YouTube Transcript API – Transcript extraction
- python-dotenv – Environment variable management

## 🏗️ Project Architecture

```text
                    YouTube URL
                         │
                         ▼
                Extract Transcript
                         │
                         ▼
                   Text Chunks
                         │
                         ▼
                Gemini Embeddings
                         │
                         ▼
                 FAISS Vector Store
                         │
                         ▼
                     Retriever
                         ▲
                         │
                    User Query
                         │
                         ▼
               Relevant Documents
                         │
                         ▼
                Prompt Augmentation
                         │
                         ▼
                Gemini 2.5 Flash
                         │
                         ▼
                   Final Answer
```
## 📁 Project Structure
```
youtube-rag-chatbot/
│
├── app.py
├── rag.py
├── youtube_utils.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```
## ⚠️ Limitations

- The YouTube video must have an accessible transcript.
- The project uses the **free tier of the Google Gemini API**, which is subject to rate limits, token limits, and daily usage quotas.
- Processing large transcripts may consume a significant amount of API quota because embeddings are generated for transcript chunks.
- FAISS vector data is created during video processing and is not permanently stored.
- The chatbot's answers depend on the quality and availability of the retrieved transcript context.
- Repeatedly processing videos or sending many queries may result in temporary API quota errors.
