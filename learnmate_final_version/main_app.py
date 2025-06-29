import streamlit as st
from utils.pdf_utils import extract_text_from_pdf
from utils.text_splitter import split_text
from sentence_transformers import SentenceTransformer, util
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

#---CONFIG---
st.set_page_config(page_title="LearnMate - PDF Q&A Bot", layout="wide")
st.title("📘 LearnMate - PDF Question Answering Bot")

# Sidebar
st.sidebar.header("Upload and Ask")
uploaded_file = st.sidebar.file_uploader("Upload a PDF", type="pdf")
question_input = st.sidebar.text_input("Type your question:")

# Sidebar: Credential Selection
st.sidebar.title("🔐 IBM Watsonx Credentials")
use_custom_creds = st.sidebar.radio(
    "Select Credential Option:",
    options=["Use default credentials", "Use my own credentials"],
    index=0
)

# Use default or allow user input
if use_custom_creds == "Use my own credentials":
    api_key = st.sidebar.text_input("🔑 IBM API Key", type="password")
    project_id = st.sidebar.text_input("🆔 IBM Project ID")
else:
    api_key = "vBVJUXhWG38XeIyiQs6OUnWY4_R8KIjdHvB4tsUg6rIC"
    project_id = "cf0c115c-5e77-471c-aede-f35fc523835c"

#---Initialize Embedding Model ------------------
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

#---Process PDF ------------------
if uploaded_file is not None:
    raw_text = extract_text_from_pdf(uploaded_file)
    chunks = split_text(raw_text, max_chunk_size=300)
    chunk_embeddings = embedding_model.encode(chunks, convert_to_tensor=True)

    st.success(f"✅ PDF loaded and split into {len(chunks)} chunks.")

    # ------------------ Q&A ------------------
    if question_input:
        question_embedding = embedding_model.encode(question_input, convert_to_tensor=True)
        similarities = util.cos_sim(question_embedding, chunk_embeddings)[0]
        best_chunk_idx = similarities.argmax()
        similarity_score = similarities[best_chunk_idx].item()
        best_chunk = chunks[best_chunk_idx]

        # Threshold logic
        THRESHOLD = 0.45
        st.caption(f"🧠 Match confidence: {similarity_score * 100:.2f}%")

        if similarity_score < THRESHOLD:
            st.warning("❗ The question doesn't seem to match the content in the document.")
            st.info("💬 Answer: Sorry, I couldn't find that information in the document.")
        else:
            with st.expander("🔍 Most relevant context (click to view)", expanded=False):
                st.code(best_chunk)

            if api_key and project_id:
                creds = Credentials(
                    api_key=api_key,
                    url="https://us-south.ml.cloud.ibm.com"
                )

                qa_model = ModelInference(
                    model_id="ibm/granite-13b-instruct-v2",
                    credentials=creds,
                    project_id=project_id,
                    params={
                        "temperature": 0.7,
                        "max_new_tokens": 600,
                        "decoding_method": "sample",
                        "top_k": 100,
                        "top_p": 0.95,
                        "repetition_penalty": 1.2
                    }
                )

                # Prompt Template
                prompt = f"""
You are an expert teaching assistant. Your job is to help students deeply understand topics using the provided study material.
Answer the question in a clear, detailed, and informative manner, covering all relevant concepts from the context. 
Include examples or elaborations if possible. If the answer is not found in the context, say: "Sorry, I couldn't find that information in the document."
Only answer based on the given context. Do not make up facts.
Context:
{best_chunk}
Question: {question_input}
Answer:
"""

                with st.spinner("🧠 Generating answer..."):
                    try:
                        response = qa_model.generate(prompt=prompt)
                        answer = response['results'][0]['generated_text'].strip()

                        st.success("✅ Answer:")
                        st.markdown(f"**{answer}**")
                    except Exception as e:
                        st.error(f"❌ Error from model: {str(e)}")
            else:
                st.warning("Please provide IBM API Key and Project ID to generate an answer.")
else:
    st.info("👈 Upload a PDF from the sidebar to get started.")
