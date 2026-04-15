import os
import re
from flask import Flask, request, render_template_string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pypdf import PdfReader

app = Flask(__name__)

# Eye-catchy modern UI with a "Glassmorphism" effect
UI_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>IRTM AI Assistant</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; display: flex; justify-content: center; }
        .main-card { width: 100%; max-width: 700px; background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); padding: 40px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); }
        h1 { color: #38bdf8; text-align: center; font-weight: 300; margin-bottom: 30px; }
        .form-section { display: flex; flex-direction: column; gap: 20px; }
        input[type="file"] { background: #1e293b; padding: 10px; border-radius: 8px; border: 1px solid #334155; color: #94a3b8; }
        .search-row { display: flex; gap: 10px; }
        input[type="text"] { flex: 1; padding: 15px; border-radius: 10px; border: none; background: #334155; color: white; outline: none; }
        button { background: #38bdf8; color: #0f172a; padding: 15px 30px; border-radius: 10px; border: none; font-weight: bold; cursor: pointer; transition: 0.3s; }
        button:hover { background: #7dd3fc; transform: scale(1.02); }
        .response-box { margin-top: 30px; padding: 20px; background: rgba(56, 189, 248, 0.1); border-left: 4px solid #38bdf8; border-radius: 8px; }
        .ref { display: block; margin-top: 15px; font-size: 0.85rem; color: #7dd3fc; font-style: italic; }
    </style>
</head>
<body>
    <div class="main-card">
        <h1>IRTM Knowledge Engine</h1>
        <form method="POST" enctype="multipart/form-data" class="form-section">
            <label>Upload Knowledge Base (PDF/TXT):</label>
            <input type="file" name="my_docs" multiple>
            
            <div class="search-row">
                <input type="text" name="my_question" placeholder="Ask a question about the uploaded files..." required>
                <button type="submit">Ask AI</button>
            </div>
        </form>

        {% if result_text %}
        <div class="response-box">
            <strong>Question:</strong> {{ question_text }} <br><br>
            <strong>Response:</strong> {{ result_text }}
            {% if origin_file %}
            <span class="ref">📍 Found in: {{ origin_file }}</span>
            {% endif %}
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

def process_file(file):
    fname = file.filename.lower()
    try:
        if fname.endswith('.txt'):
            return file.read().decode('utf-8', errors='ignore')
        if fname.endswith('.pdf'):
            reader = PdfReader(file)
            content = ""
            for page in reader.pages:
                content += page.extract_text() or ""
            return content
    except Exception:
        return ""
    return ""

@app.route('/', methods=['GET', 'POST'])
def home():
    # Context dictionary to pass to template
    data_packet = {
        "question_text": "",
        "result_text": "",
        "origin_file": ""
    }
    
    if request.method == 'POST':
        data_packet["question_text"] = request.form.get('my_question')
        uploaded_files = request.files.getlist('my_docs')
        
        corpus = []
        file_refs = []
        
        for f in uploaded_files:
            if f.filename != '':
                text_data = process_file(f)
                # Tokenize into sentences using regex
                sentences = re.split(r'(?<=[.!?]) +', text_data)
                for s in sentences:
                    clean_s = s.strip()
                    if len(clean_s) > 20: # Filter out very short lines
                        corpus.append(clean_s)
                        file_refs.append(f.filename)

        if corpus and data_packet["question_text"]:
            # IRTM Engine Implementation
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(corpus)
            query_vec = vectorizer.transform([data_packet["question_text"]])
            
            # Find Similarity
            similarity = cosine_similarity(query_vec, tfidf_matrix).flatten()
            best_match_index = similarity.argmax()
            
            if similarity[best_match_index] > 0.1:
                data_packet["result_text"] = corpus[best_match_index]
                data_packet["origin_file"] = file_refs[best_match_index]
            else:
                data_packet["result_text"] = "I couldn't find a relevant answer in the provided documents."
        else:
            data_packet["result_text"] = "Please upload files containing text to get an answer."

    # Using dictionary unpacking to prevent any argument conflicts
    return render_template_string(UI_HTML, **data_packet)

if __name__ == '__main__':
    app.run(debug=True)