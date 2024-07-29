# Hammett Plot Data Analysis and Visualization Tool

## Project Overview
The main goal of this project is to facilitate the analysis of chemistry-related literature. Users can provide specified papers, questions, and data, and the program will generate answers by comprehensively reading and analyzing the paper. This project leverages the capabilities of the Gemini API and the mistralai/Mistral-7B-Instruct-v0.1 model to enhance data analysis and insights generation.

## Key Features
- Generating Hammett plot graphs: Based on user-selected substituents.
- Downloading graph data: For further analysis.
- Detailed analysis and insight generation: Using the downloaded data in conjunction with the paper and specified questions.
- Advanced AI Integration: Utilizes the Gemini API for enhanced data handling and mistralai/Mistral-7B-Instruct-v0.1 model for superior natural language processing capabilities.

## Technology Integration
- Gemini API: Utilized to generate the final answers and analysis based on the provided pages.
- mistralai/Mistral-7B-Instruct-v0.1: Employed to identify relevant pages in the paper related to the questions and generate preliminary answers.

## Installation

### Using Terminal

If you are running in the terminal, please execute the following commands:

    git clone https://github.com/ArthurArthurArthur0817/LLM-RAG.git

Next, execute the following commands to set up the environment:

    pip install -r requirements.txt

After completion, run the following program to get the web URL:

    python app.py

### Using an IDE

If you are using an IDE (such as VSCode, etc.), please download all the above files and ensure the files are placed in the following order:

 ```
project/
├── app.py
├── gemini.py
├── mistral-7B-instruct.py
├── hammett_plot.py
├── Table_1.xlsx
├── uploads/
└── faiss_index_py/
    ├── index.faiss
    └── index.pkl
└── __pycache__/
    └── hammett_plot.cpython-310.pyc
└── templates/
    ├── hammett_plot.html
    ├── index.html
    ├── plot_result.html
    └── result.html
```

After confirming, make sure to execute the following command in the terminal to set up the environment:

    pip install -r requirements.txt

After executing, run the **app.py** file to get the web URL.

### Using API Key

To ensure proper functionality of the program, please replace the placeholder data with your own API keys and access tokens in the following lines of code:

gemini.py

    api_key = 'Your Gemini API KEY'
    
minstral-7B-instruct.py

    os.environ["HUGGINGFACEHUB_API_TOKEN"] = "Your HuggingFace Access Token"


### Warning

If your gemini.py displays "No text extracted from the provided sources for question:" during execution, please use the gemini.py from this [link](https://github.com/ArthurArthurArthur0817/Educational-Big-Data/blob/main/gemini.py(for%20google%20VM)) to replace the program.


## User Guide
[Project Intoduction/Demonstration Video](https://youtu.be/eci8HjQMh_I)


**Chart Generation:**

     1.Select the Hammett Plot Generation section and click "Generate the plot" to begin.

2.Enter the y-axis label and select whether to take the logarithm of the data. The x-axis will be fixed to the substituent's σp value.

3.Input the substituents and their corresponding values for plotting. Click "Add new row" to add more entries.

4.Once done, click "Generate Plot" to view the chart. You can download the chart by clicking "Download the plot" and obtain the chart data in JSON format by clicking "Download the data".

**Question Answering:**

1.Navigate to the Upload PDF and Question File section.

2.Upload any number of PDF files in the "Select PDF Document" section, and upload an XLSX file containing the questions in the "Select Question Excel File" section. The question file should have 

3.a column named "question" with multiple questions listed under it.

4.Click "upload" to start the file reading and answer generation process. This may take 2-3 minutes. Once completed, you can download the generated answers file.

**Data Analysis:**

1.Use the JSON file obtained from the **"Chart Generation"** section, and add it to the column "data" in the question XLSX file. Refer to the file format in the **"Usage Example"** section below.

2.Upload the XLSX file containing both questions and data using the instructions provided in the **"Question Answering"** section.

### Usage Example
Here is a simple example to help you get started with using the project:

[Example](https://github.com/ArthurArthurArthur0817/LLM-RAG/blob/main/Example.pdf)







