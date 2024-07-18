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


## QA
### First edition
[mistralaiMistral-7B-Instruct-v0.1](https://github.com/ArthurArthurArthur0817/LLM-RAG/blob/main/QA(mistralaiMistral-7B-Instruct-v0.1)_Dennis.docx)

[microsoftPhi-3-mini-4k-instruct](https://github.com/ArthurArthurArthur0817/LLM-RAG/blob/main/QA(microsoftPhi-3-mini-4k-instruct)_Dennis.docx)



