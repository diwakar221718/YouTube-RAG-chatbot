# rag.py

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)

from langchain_community.vectorstores import FAISS

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# 1. Gemini LLM
# ============================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


# ============================================================
# 2. Gemini Embedding Model
# ============================================================

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)


# ============================================================
# 3. Create Vector Store
# ============================================================

def create_vector_store(transcript, video_id=None):

    # Create a LangChain Document
    document = Document(
        page_content=transcript,
        metadata={
            "video_id": video_id
        }
    )

    # --------------------------------------------------------
    # Text Splitter
    # --------------------------------------------------------

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(
        [document]
    )

    print(f"Number of chunks created: {len(chunks)}")

    # --------------------------------------------------------
    # Create FAISS Vector Store
    # --------------------------------------------------------

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    return vector_store


# ============================================================
# 4. Create Retriever
# ============================================================

def create_retriever(vector_store):

    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": 4
        }
    )

    return retriever


# ============================================================
# 5. Prompt Template
# ============================================================

prompt = PromptTemplate(
    template="""
You are a helpful YouTube video assistant.

Answer the user's question ONLY using the
provided transcript context.

Do not use outside knowledge.

If the answer is not available in the transcript,
say:

"I don't know based on the provided video."

Keep the answer clear and concise.

--------------------
Transcript Context:
{context}
--------------------

Question:
{question}

Answer:
""",
    input_variables=[
        "context",
        "question"
    ]
)


# ============================================================
# 6. Format Retrieved Documents
# ============================================================

def format_docs(docs):

    return "\n\n".join(
        doc.page_content
        for doc in docs
    )


# ============================================================
# 7. Create RAG Chain
# ============================================================

def create_rag_chain(vector_store):

    # Create retriever
    retriever = create_retriever(
        vector_store
    )

    # RAG chain
    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain