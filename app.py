from flask import Flask, request, render_template, send_file, send_from_directory, redirect, url_for
import os
import subprocess
import threading
import pandas as pd

app = Flask(__name__)

# 文件上傳目錄
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

lock = threading.Lock()

# 預設的 PDF 文件路徑
PDF_DEFAULT_PATH = r"./Hansch_merged.pdf"


@app.route('/')
def index():
    return render_template('index.html')

# 定義一個路由來提供 CSS 文件
@app.route('/css/<path:filename>')
def send_css(filename):
    return send_from_directory('css', filename)

@app.route('/upload', methods=['POST'])
def upload_files():
    with lock:
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

        # 调用 mistral-7B-instruct.py
        mistral_command = f"python mistral-7B-instruct.py {question_path} {' '.join(pdf_paths)}"
        subprocess.run(mistral_command, shell=True)

        # 调用 gemini.py
        gemini_command = "python gemini.py"
        subprocess.run(gemini_command, shell=True)

        return render_template('results.html')


@app.route('/download')
def download_file():
    path = "gemini_responses.txt"
    return send_file(path, as_attachment=True)

@app.route('/hammett')
def hammett():
    return render_template('hammett_plot.html')

@app.route('/plot', methods=['POST'])
def plot():
    from hammett_plot import generate_hammett_plot

    y_axis_label = request.form['y_axis_label']
    log_transform = request.form.get('log_transform') == 'true'
    sigma_type = request.form['sigma_type']

    substituents = []
    values = []

    if 'data_file' in request.files and request.files['data_file'].filename != '':
        data_file = request.files['data_file']
        df = pd.read_excel(data_file)
        substituents = df['substituent'].tolist()
        values = df['value'].tolist()
    else:
        for key in request.form:
            if key.startswith('substituent'):
                substituents.append(request.form[key])
            elif key.startswith('value'):
                values.append(request.form[key])

    with lock:
        image_path, output_path = generate_hammett_plot(substituents, values, y_axis_label, log_transform, sigma_type, app.config['UPLOAD_FOLDER'])

        if os.path.exists(output_path) and os.path.exists(PDF_DEFAULT_PATH):
            mistral_command = f"python mistral-7B-instruct.py {output_path} {PDF_DEFAULT_PATH}"
            subprocess.run(mistral_command, shell=True)

            gemini_command = "python gemini.py"
            subprocess.run(gemini_command, shell=True)
        else:
            return "Output XLSX or default PDF not found", 404

    return render_template('plot_result.html', image_path=image_path, output_path=output_path)

# 新增路由，負責將用戶輸入的數據寫入到 Table_1.xlsx
@app.route('/write_data', methods=['POST'])
def write_data():
    substituent = request.form.get('substituent')
    sigma_m = request.form.get('sigma_m')
    sigma_p = request.form.get('sigma_p')

    data_file = 'Table_1.xlsx'

    # 讀取現有的 Excel 文件
    df = pd.read_excel(data_file)

    # 新數據為一個 DataFrame
    new_data = pd.DataFrame({
        'substituent': [substituent],
        'σm': [sigma_m],
        'σp': [sigma_p]
    })

    # 使用 concat 將新數據添加到現有數據
    df = pd.concat([df, new_data], ignore_index=True)

    # 保存修改後的 Excel 檔案
    df.to_excel(data_file, index=False)

    return redirect(url_for('hammett'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
