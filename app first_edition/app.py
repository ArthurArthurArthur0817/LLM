from flask import Flask, request, render_template, send_file
import os
import pandas as pd
import subprocess

app = Flask(__name__)

# 文件上傳目錄
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'pdf_files' not in request.files or 'question_file' not in request.files:
        return "No file part", 400

    pdf_files = request.files.getlist('pdf_files')
    question_file = request.files['question_file']

    pdf_paths = []
    for pdf_file in pdf_files:
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
        pdf_file.save(pdf_path)
        pdf_paths.append(pdf_path)

    question_path = os.path.join(app.config['UPLOAD_FOLDER'], question_file.filename)
    question_file.save(question_path)

    # 調用 mistral-7B-instruct.py
    mistral_command = f"python mistral-7B-instruct.py {question_path} {' '.join(pdf_paths)}"
    subprocess.run(mistral_command, shell=True)

    # 調用 gemini.py
    gemini_command = "python gemini.py"
    subprocess.run(gemini_command, shell=True)

    return render_template('results.html')

@app.route('/download')
def download_file():
    path = "gemini_responses.txt"
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
