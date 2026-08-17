# app.py

import streamlit as st

from youtube_utils import get_transcript_from_url
from rag import create_vector_store, create_rag_chain


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="YouTube Chatbot",
    page_icon="🎥",
    layout="wide"
)


# ============================================================
# Title
# ============================================================

st.title("🎥 YouTube RAG Chatbot")

st.write(
    "Enter a YouTube video URL and ask questions about its content."
)


# ============================================================
# Session State Initialization
# ============================================================

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None

if "video_id" not in st.session_state:
    st.session_state.video_id = None

if "transcript" not in st.session_state:
    st.session_state.transcript = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.header("🎬 Video")

    youtube_url = st.text_input(
        "Enter YouTube URL",
        placeholder="https://www.youtube.com/watch?v=..."
    )

    process_video = st.button(
        "Process Video",
        use_container_width=True
    )

    # --------------------------------------------------------
    # Clear Chat
    # --------------------------------------------------------

    if st.button(
        "Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# ============================================================
# Process YouTube Video
# ============================================================

if process_video:

    if not youtube_url.strip():

        st.error(
            "Please enter a YouTube video URL."
        )

    else:

        # ----------------------------------------------------
        # Step 1: Get Transcript
        # ----------------------------------------------------

        with st.spinner(
            "Fetching YouTube transcript..."
        ):

            transcript, video_id, error = (
                get_transcript_from_url(
                    youtube_url
                )
            )

        # ----------------------------------------------------
        # Transcript Error
        # ----------------------------------------------------

        if error:

            st.error(error)

        else:

            st.success(
                "Transcript retrieved successfully!"
            )

            # Store transcript
            st.session_state.transcript = transcript

            # Store video ID
            st.session_state.video_id = video_id

            # ------------------------------------------------
            # Step 2: Create Vector Store
            # ------------------------------------------------

            with st.spinner(
                "Creating embeddings and vector store..."
            ):

                try:

                    vector_store = create_vector_store(
                        transcript,
                        video_id
                    )

                    st.session_state.vector_store = (
                        vector_store
                    )

                except Exception as e:

                    st.error(
                        f"Error creating vector store: {e}"
                    )

                    st.stop()

            # ------------------------------------------------
            # Step 3: Create RAG Chain
            # ------------------------------------------------

            with st.spinner(
                "Creating RAG chain..."
            ):

                try:

                    rag_chain = create_rag_chain(
                        vector_store
                    )

                    st.session_state.rag_chain = (
                        rag_chain
                    )

                except Exception as e:

                    st.error(
                        f"Error creating RAG chain: {e}"
                    )

                    st.stop()

            # ------------------------------------------------
            # Clear Previous Chat
            # ------------------------------------------------

            st.session_state.messages = []

            st.success(
                "✅ Video processed successfully!"
            )

            st.info(
                "You can now ask questions about the video."
            )


# ============================================================
# Video Information
# ============================================================

if st.session_state.video_id:

    st.subheader("📺 Current Video")

    st.write(
        f"**Video ID:** {st.session_state.video_id}"
    )

    if st.session_state.transcript:

        transcript_length = len(
            st.session_state.transcript
        )

        st.write(
            f"**Transcript:** {transcript_length:,} characters"
        )


# ============================================================
# Display Chat History
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# Chat Input
# ============================================================

question = st.chat_input(
    "Ask something about the video..."
)


# ============================================================
# Handle User Question
# ============================================================

if question:

    # --------------------------------------------------------
    # Check if video has been processed
    # --------------------------------------------------------

    if st.session_state.rag_chain is None:

        st.warning(
            "⚠️ Please enter a YouTube URL and process "
            "the video first."
        )

    else:

        # ----------------------------------------------------
        # Display User Question
        # ----------------------------------------------------

        with st.chat_message("user"):

            st.markdown(question)

        # Save user message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        # ----------------------------------------------------
        # Generate Answer
        # ----------------------------------------------------

        with st.chat_message("assistant"):

            with st.spinner(
                "Searching the video and generating answer..."
            ):

                try:

                    answer = (
                        st.session_state.rag_chain.invoke(
                            question
                        )
                    )

                    st.markdown(answer)

                except Exception as e:

                    answer = (
                        "Sorry, I encountered an error "
                        f"while generating the answer: {e}"
                    )

                    st.error(answer)

        # ----------------------------------------------------
        # Save Assistant Message
        # ----------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )