from config import model
from langchain.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
import os
import streamlit as st

class FutureWorksAgent:
    def __init__(self):
        self.model = model
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.prompt = """Generate ideas for future research to be included in a review paper. 
        Provide a well-structured summary that highlights opportunities for future work and potential improvements.
        
        Chat history:
        {chat_history}
        
        Research context:
        {context}
        
        Guidelines:
        1. Determine if the query seeks a combined review or specific future directions.
        2. For future directions:
            a. Summarize key opportunities and limitations from papers
            b. Generate improvement plans and suggest novel contributions
        3. For paper reviews:
            a. Provide comprehensive combined review with sections
            b. Create cohesive research roadmap
        4. Discuss technical challenges and methodological improvements
        5. Highlight potential applications and research gaps
        """
    
    def solve(self, query):
        if not os.path.exists("vdb_chunks"):
            return "Please search for papers first before asking about future works."
        
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
                context=context
            )
            
            response = self.model.generate_content(full_prompt)
            return response["content"]
            
        except Exception as e:
            return f"Error processing query: {str(e)}"