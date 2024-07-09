from flask import Flask, request, render_template, send_file, send_from_directory
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import subprocess
import json

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

@app.route('/hammett')
def hammett():
    return render_template('hammett_plot.html')

@app.route('/plot', methods=['POST'])
def plot():
    y_axis = request.form['y_axis']
    plot_file = request.files['plot_file']
    plot_path = os.path.join(app.config['UPLOAD_FOLDER'], plot_file.filename)
    plot_file.save(plot_path)

    # 讀取data.xlsx
    data_file = 'data.xlsx'
    df_data = pd.read_excel(data_file)
    sigma_values = df_data.set_index('substituent')['σ'].to_dict()

    # 讀取plot.xlsx
    df_plot = pd.read_excel(plot_path)

    def plot_hammett(x_data, y_data, subs, title, xlabel, ylabel, slope, intercept, r_squared):
        plt.figure(figsize=(10, 6))
        plt.scatter(x_data, y_data)
        for i, txt in enumerate(subs):
            plt.annotate(txt, (x_data[i], y_data[i]))
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        # 繪製回歸線
        plt.plot(x_data, slope * np.array(x_data) + intercept, color='red')

        # 顯示回歸線方程式及R²值
        equation_text = f'y = {slope:.2f}x + {intercept:.2f}\n$R^2$ = {r_squared:.2f}'
        plt.text(0.05, 0.95, equation_text, transform=plt.gca().transAxes, fontsize=12, verticalalignment='top')

        plt.grid(True)
        plt.savefig(os.path.join(app.config['UPLOAD_FOLDER'], 'hammett_plot.png'))
        plt.close()

    # 準備數據
    sigma = [sigma_values[sub] for sub in df_plot['substituent']]
    
    # 轉換數據類型
    if y_axis == 'log_kx_kh':
        y_data = np.log10(pd.to_numeric(df_plot['log(KX/KH)'], errors='coerce')).tolist()
    elif y_axis == 'kx_kh':
        y_data = np.log10(pd.to_numeric(df_plot['KX/KH'], errors='coerce')).tolist()
    elif y_axis == 'rate':
        y_data = np.log10(pd.to_numeric(df_plot['Rate'], errors='coerce')).tolist()

    # 確保sigma也是浮點數類型
    sigma = pd.to_numeric(sigma, errors='coerce').tolist()

    # 線性回歸
    X = np.array(sigma).reshape(-1, 1)
    y = np.array(y_data)
    reg = LinearRegression().fit(X, y)
    slope = reg.coef_[0]
    intercept = reg.intercept_
    r_squared = r2_score(y, reg.predict(X))

    plot_hammett(sigma, y_data, df_plot['substituent'].tolist(), 'Hammett Plot', 'σ', y_axis, slope, intercept, r_squared)

    # 準備數據以JSON格式存儲
    data_json = {
        "substituent": df_plot['substituent'].tolist(),
        "log(KX/KH)": df_plot['log(KX/KH)'].tolist(),
        "σ": sigma,
        "ρ": slope,
        "R²": r_squared
    }

    # 生成output.xlsx
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.xlsx')
    df_output = pd.DataFrame({'data': [json.dumps(data_json, ensure_ascii=False)]})
    df_output.to_excel(output_path, index=False)

    return render_template('plot_result.html', image_path='uploads/hammett_plot.png', output_path='uploads/output.xlsx')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
