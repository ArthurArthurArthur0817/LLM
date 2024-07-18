# Hammett Plot Data Analysis and Visualization Tool

## Project Overview
The main goal of this project is to facilitate the analysis of chemistry-related literature. Users can provide specified papers, questions and data, the program will generate answers by comprehensively reading and analyzing the paper.

## Key features 

- Generating Hammett plot graphs based on user-selected substituents.
- Downloading graph data for further analysis.
- Using the downloaded data in conjunction with the paper and specified question for detailed analysis and insight generation.

## Installation

**STEP 1**

    pip install -r requirements.txt

**STEP 2**

To ensure proper functionality of the program, please replace the placeholder data with your own API keys and access tokens in the following lines of code:

gemini.py

    api_key = 'Your Gemini API KEY'
    
minstral-7B-instruct.py

    os.environ["HUGGINGFACEHUB_API_TOKEN"] = "Your HuggingFace Access Token"

### File

Ensure that your files and folders are organized as follows:

 ```
project/
├── app.py
├── gemini.py
├── mistral-7B-instruct.py
├── hammett_plot.py
├── Table_1.xlsx
├── uploads/
└── templates/
    ├── hammett_plot.html
    ├── index.html
    ├── plot_result.html
    └── result.html
```

### User Guide
[Project Intoduction/Demonstration Video](https://youtu.be/eci8HjQMh_I)


**Chart Generation:**

Select the Hammett Plot Generation section and click "Generate the plot" to begin.
Enter the y-axis label and select whether to take the logarithm of the data. The x-axis will be fixed to the substituent's σp value.
Input the substituents and their corresponding values for plotting. Click "Add new row" to add more entries.
Once done, click "Generate Plot" to view the chart. You can download the chart by clicking "Download the plot" and obtain the chart data in JSON format by clicking "Download the data".

**Question Answering:**

Navigate to the Upload PDF and Question File section.
Upload any number of PDF files in the "Select PDF Document" section, and upload an XLSX file containing the questions in the "Select Question Excel File" section. The question file should have a column named "question" with multiple questions listed under it.
Click "upload" to start the file reading and answer generation process. This may take 2-3 minutes. Once completed, you can download the generated answers file.

**Data Analysis:**

Use the JSON file obtained from the "Chart Generation" section, and add it to the column "data" in the question XLSX file. Refer to the file format in the "Usage Example" section below.
Upload the XLSX file containing both questions and data using the instructions provided in the "Question Answering" section.

### Usage Example
Here is a simple example to help you get started with using the project:

[Example](https://github.com/ArthurArthurArthur0817/LLM-RAG/blob/main/Example.pdf)



## QA
### First edition
[mistralaiMistral-7B-Instruct-v0.1](https://github.com/ArthurArthurArthur0817/LLM-RAG/blob/main/QA(mistralaiMistral-7B-Instruct-v0.1)_Dennis.docx)

[microsoftPhi-3-mini-4k-instruct](https://github.com/ArthurArthurArthur0817/LLM-RAG/blob/main/QA(microsoftPhi-3-mini-4k-instruct)_Dennis.docx)



