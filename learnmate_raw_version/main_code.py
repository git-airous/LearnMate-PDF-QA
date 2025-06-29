#---install required lib---
!pip install -U sentence-transformers
!pip install -U pdfplumber
!pip install -U ibm-watsonx-ai


#---helper files---
import os

os.makedirs("utils", exist_ok=True)

with open("utils/pdf_utils.py", "w") as f:
    f.write('''
import pdfplumber

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + "\\n"
    return text
''')

with open("utils/text_splitter.py", "w") as f:
    f.write('''
def split_text(text, max_chunk_size=300):
    paragraphs = text.split("\\n")
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) <= max_chunk_size:
            current_chunk += para + "\\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para + "\\n"
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks
''')
    

#---main code---
from utils.pdf_utils import extract_text_from_pdf
from utils.text_splitter import split_text
from sentence_transformers import SentenceTransformer, util
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
import torch

# Load models
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# IBM watsonx credentials (default, feel free to change)
api_key = "vBVJUXhWG38XeIyiQs6OUnWY4_R8KIjdHvB4tsUg6rIC"
project_id = "cf0c115c-5e77-471c-aede-f35fc523835c"

creds = Credentials(api_key=api_key, url="https://us-south.ml.cloud.ibm.com")

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


#---upload and process PDF---
from google.colab import files

print("Upload a PDF file")
uploaded = files.upload()

pdf_path = list(uploaded.keys())[0]
raw_text = extract_text_from_pdf(pdf_path)

chunks = split_text(raw_text, max_chunk_size=300)
chunk_embeddings = embedding_model.encode(chunks, convert_to_tensor=True)

print(f"Loaded! Total chunks: {len(chunks)}")


#---ask questions---
def ask_question(question):
    question_embedding = embedding_model.encode(question, convert_to_tensor=True)
    similarities = util.cos_sim(question_embedding, chunk_embeddings)[0]
    best_idx = torch.argmax(similarities).item()
    best_chunk = chunks[best_idx]
    score = similarities[best_idx].item()

    print(f"\nMatch confidence: {score * 100:.2f}%")

    if score < 0.45:
        print("Answer: Sorry, I couldn't find that information in the document.")
        return

    prompt = f"""
You are an expert teaching assistant. Your job is to help students deeply understand topics using the provided study material.
Answer the question in a clear, detailed, and informative manner, covering all relevant concepts from the context. 
Include examples or elaborations if possible. If the answer is not found in the context, say: "Sorry, I couldn't find that information in the document."
Only answer based on the given context. Do not make up facts.

Context:
{best_chunk}

Question: {question}
Answer:
"""

    response = qa_model.generate(prompt=prompt)
    answer = response['results'][0]['generated_text'].strip()
    print(f"Answer:\n ->{answer}")


#---simple chat loop---
while True:
    q = input("\nQ: Ask a question (or type 'exit'): ").strip()
    if q.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break
    ask_question(q)