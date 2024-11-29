from config import model
from langchain_ollama import OllamaEmbeddings
from langchain.vectorstores import FAISS
import os
import streamlit as st 
from agents import  SearchAgent


            
embeddings = OllamaEmbeddings(model="nomic-embed-text")

class QAAgent:
    def __init__(self):
        
        self.model = model
        self.prompt = """You are a research assistant answering questions about academic papers. Use the following context from papers and chat history to provide accurate, specific answers.

        Previous conversation:
        {chat_history}

        Paper context:
        {context}

        Question: {question}

        Guidelines:
        1. Reference specific papers with particular section names when making claims
        2. Use direct quotes when relevant and give the paper and section names
        3. Acknowledge if information isn't available in the provided context
        4. Maintain academic tone and precision
        5. Mention specific key-words, figures or tables from papers whenever needed
        """

    def solve(self, query):
        if not os.path.exists("vdb_chunks"):
            return "Please search for papers first before asking questions."
        
        try:
            # Load vector store
            vdb_chunks = FAISS.load_local(
                "vdb_chunks", 
                self.embeddings,
                index_name="base_and_adjacent",
                allow_dangerous_deserialization=True
            )
            
            # Get chat history
            chat_history = st.session_state.get("chat_history", [])
            chat_history_text = "\n".join([f"{sender}: {msg}" for sender, msg in chat_history[-5:]])
            
            # Get relevant chunks
            retrieved = vdb_chunks.as_retriever().get_relevant_documents(query)
            context = "\n".join([f"{doc.page_content} Source: {doc.metadata['source']}" 
                               for doc in retrieved])
            
            # Generate response
            full_prompt = self.prompt.format(
                chat_history=chat_history_text,
                context=context,
                question=query
            )
            
            response = self.model.generate_content(full_prompt)
            return response["content"]
            
        except Exception as e:
            return f"Error processing query: {str(e)}"