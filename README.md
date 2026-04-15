# K02_IRTM_PRACTICAL

# 📘 IRTM Knowledge Engine (AI Assistant)

## 🚀 Overview

The **IRTM Knowledge Engine** is a simple AI-powered web application that allows users to upload documents (PDF/TXT) and ask questions based on their content.

It uses **Information Retrieval and Text Mining (IRTM)** concepts like **TF-IDF** and **Cosine Similarity** to find the most relevant answer from the uploaded files.

---

## 🧠 Features

* 📂 Upload multiple **PDF or TXT files**
* ❓ Ask questions related to uploaded documents
* 🔍 Uses **TF-IDF Vectorization** for text representation
* 📊 Uses **Cosine Similarity** to find best match
* 🎯 Returns the **most relevant sentence**
* 📍 Shows **source file name**
* ✨ Modern UI with **Glassmorphism design**

---

## 🛠️ Tech Stack

* **Backend:** Flask (Python)
* **ML/NLP:**

  * TF-IDF → `TfidfVectorizer`
  * Similarity → `cosine_similarity`
* **PDF Processing:** `pypdf`
* **Frontend:** HTML + CSS (embedded)

---

## ⚙️ How It Works

1. User uploads documents (PDF/TXT)
2. Text is extracted and split into sentences
3. Sentences are converted into vectors using TF-IDF
4. User query is also vectorized
5. Cosine similarity is calculated
6. The most similar sentence is returned as the answer

---

## 📦 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-link>
cd irtm-knowledge-engine
```

### 2️⃣ Install Dependencies

```bash
pip install flask scikit-learn pypdf
```

### 3️⃣ Run the Application

```bash
python irtm_app.py
```

### 4️⃣ Open in Browser

```
http://127.0.0.1:5000/
```

---

## 📁 Project Structure

```
irtm_app.py       # Main Flask application
README.md         # Project documentation
```

---

## 📊 Core Concepts Used

* **TF (Term Frequency)** – Frequency of word in document
* **IDF (Inverse Document Frequency)** – Importance of word
* **TF-IDF** – Weighted importance of words
* **Cosine Similarity** – Measures similarity between query and text

---

## 📌 Limitations

* Works only on **sentence-level matching**
* No deep semantic understanding (not using transformers)
* Performance depends on document quality

---

## 🔥 Future Improvements

* Add **BERT / LLM-based semantic search**
* Store documents in **vector database (FAISS)**
* Add **user authentication**
* Improve UI with React frontend
* Support more file formats (DOCX, HTML)

---

## 🎯 Use Cases

* Resume vs Job Description matching
* Study material Q&A
* Document search engine
* Knowledge base assistant

---

## 👨‍💻 Author

Dinesh Shivaji Bodhapalle


