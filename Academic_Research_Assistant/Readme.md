# Academic-Research-Assistant

An intelligent multi-agent system that helps researchers search, analyze, explain and summarize academic papers using Large Language Models (LLMs). The application provides multi-agent capabilities for paper search, multiple pdf handling with question answering, summarization, and future research direction generation.

[Watch the Project Demonstration on YouTube](https://youtu.be/H2j2od2Dx34)

## Features

- **Paper Search**: Search and retrieve relevant research papers from Arxiv using arxiv api
- **Vector Store**: Store the retrived pdf as inmemory faiss database for efficient question answering
- **Question Answering**: Get answers about specific papers or content with source citations
- **Paper Explanation**: Get explaination of Tables, Figures and Diagrams from the papers
- **Summarization**: Extract key findings and trends from multiple papers
- **Future Works Generation**: Generate research directions and improvement plans
- **Interactive UI**: User-friendly Streamlit interface for paper browsing and chat

## Architecture

The application uses a multi-agent system with the following components:

- **Master**: Classifies user queries to choose specific and specialized agents for different tasks
- **Search Agent**: Retrieves and processes papers from Arxiv and do chunk loading in the faiss vector database
- **QA Agent**: Handles specific questions about paper content using faiss vectorstore
- **Future Works Agent**: Generates future research directions and give comprehensive review of the papers

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **LLM Integration**: Google GenAI LLM
- **Vector Store**: FAISS
- **Document Processing**: LangChain
- **PDF Processing**: PDFMiner



### Running the Local Ollama Implementation
To run the local Ollama implementation, use the following command:

```bash
# Step 1: Install Ollama CLI
curl -sSL https://ollama.com/download.sh | sh

# Step 2: Start the Ollama server
ollama serve

# Step 3: Pull a specific model
ollama pull qwen2.5  # or replace llama2 with your desired model

# Step 4: Verify installed models
ollama models

# Step 5: Install requirements.txt
pip install - r requirements.txt

# Step 6: Run Streamlit app
streamlit run local_implement_ollama/app_ollama.py
```


## Usage

1. Start the application:
```bash
streamlit run app1.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Enter your research topic or question in the chat interface

4. Select papers of interest from the timeline view

5. Interact with the assistant through queries

## Example Queries

- "Find recent papers about transformer architectures in NLP"
- "What methodology was used in the paper 'Attention is All You Need'?"
- "What are emerging trends in reinforcement learning?"
