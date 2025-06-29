# 📘 LearnMate - PDF Question Answering Bot

LearnMate is an AI-powered assistant that helps you **ask questions from any PDF document** and get precise answers based on the content inside. It uses **sentence-transformer embeddings** for semantic similarity, and IBM’s **watsonx.ai Granite LLM** for generating detailed answers.

This project contains two versions:
- ✅ A **minimalistic, terminal-based Colab version** for rapid testing.
- 🎯 A **user-friendly Streamlit app** with upload and interface support.

---

## 📌 Features

- Upload a PDF file and ask questions from it.
- Finds the **most relevant paragraph** using embeddings (`all-MiniLM-L6-v2`).
- Sends that context to IBM watsonx.ai’s **Granite-13b-Instruct-v2** model.
- Supports both **custom** and **default API credentials**.
- Handles unmatched questions gracefully.

---

## ⚡ Version 1: Colab Terminal App (`learnmate_raw_version`)

A simple CLI-like version perfect for fast experimentation or revision — no GUI, just upload, type, and get answers.

### ▶️ How to Run in Google Colab

1. **Upload your PDF** (e.g., `sample_note.pdf`).
2. **Then simply ask questions**.
3. **if the confidence is above 0.45 the model answer else it gives a sorry msg**
4. **To exit the loop enter ‘exit’ or ‘quite’**
<p>
  <i>It looks something like this:</i>
  <br>
  <img src="https://github.com/user-attachments/assets/d52c85b0-eb48-4132-a86c-8b8d894c77e9" alt="colab_terminal" width="600"/>
  <br>
</p>

---

## ⚡ Version 2: Streamlit App (`learnmate_final_version`)

This version includes a sleek web interface powered by Streamlit. You can upload PDFs, ask questions, and get structured, long-form answers with confidence scoring and context viewing.

### ▶️ How to Run in VS Code
1. **Clone the repository and navigate to the Streamlit app directory:**
```
git clone https://github.com/your-username/LearnMate-PDF-QA.git
cd LearnMate-PDF-QA/streamlit/learnmate_final_version
```
2. **Run the Streamlit application using the following command in your terminal:**
```
streamlit run main_app.py
```
This will start a local development server, and you’ll receive a URL (usually http://localhost:8501) to access the app in your browser.
3. **With every instruction please wait until the webs top right corner:**
<table>
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/6e607ba0-4fe8-4d29-bf99-ce96d09b26b3" alt="loading_icon" width="300"/><br>
    </td>
    <td>&nbsp;&nbsp;&nbsp;</td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/f1907f73-a5a1-4386-8a58-ad054bff09c0" width="40"/><br>
    </td>
    <td>&nbsp;&nbsp;&nbsp;</td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/71687e75-dd81-4017-b76a-c1c2cb4bce69" alt="loaded_icon" width="300"/><br>
    </td>
  </tr>
</table>

<p>
  <i>Finally it looks something like this:</i>
  <br>
  <img src="https://github.com/user-attachments/assets/6fd418f0-8d7a-45ba-bf7e-f565e94a4205" alt="streamlit_app" width="600"/>
  <br>
</p>

---

## 🚀 Why LearnMate?
Whether you're revising class notes, exploring a new topic, or building a smart assistant for your own PDFs, LearnMate helps you extract meaningful, contextual insights — all without searching manually through the document.

---

##🔐 API Usage Notes
This app uses IBM watsonx.ai. You can choose to:
•	Use the default API key and project ID (built-in, limited).
•	Add your own credentials for extended or private use.

---

## 📮 Contributing / Issues
If you have suggestions or want to report a bug, feel free to:
•	Open an issue here on GitHub
•	Fork the repo and make a pull request

---

## 🪪 License
This project is licensed under the MIT License.

---

## ✨ Maintained with ❤️ by @git-zeno
Let me know once you've added this, and I can help with:
- Uploading screenshots for both versions
- Writing GitHub repo descriptions and topics
