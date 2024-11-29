from config import model
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import streamlit as st
import os

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = "AIzaSyATTd-PXZRg3AG9IATYnicTF5hAA4T1zG8"
            
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

class IntentAgent:
    def __init__(self):
        self.model = model
        self.prompt = """You are an intent classifier for a research paper assistant. Given a user query, classify it into one of these categories:
        - "search": User wants to find relevant research papers on a topic
        - "qa": User has questions about specific papers or content
        - "future_works": User wants to know about future research directions
        
        Example queries and their intents:
        "Find papers about machine learning" -> "search"
        "What does the paper say about the methodology?" -> "qa"
        "What are the future research directions in this field?" -> "future_works"
        
        Respond with just the intent category.
        
        Query: {query}"""
    
    def get_intent(self, query):
        response = self.model.generate_content(self.prompt.format(query=query))
        return response.text.strip().lower()

class SearchAgent:
    def __init__(self):
        self.model = model
        self.prompt = """Extract the core research topic or paper details from the following query. Focus on the main subject matter and any specific paper details mentioned.
        
        If it's a general topic search:
        - Return just the topic (e.g., "Machine Learning for Healthcare")
        
        If it's about a specific paper:
        - Include title, author(s), and year if mentioned
        
        Query: {query}"""
        
    def solve(self, query):
        if not os.path.exists("vdb_chunks"):
            print("Creating new vector database...")
            # Your existing paper fetching and processing code here
            
        papers = self.fetch_papers(query)  # Your existing paper fetching logic
        
        # Store papers in session state for other agents
        if "fetched_papers" not in st.session_state:
            st.session_state.fetched_papers = papers
            
        return papers, papers

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
        1. Reference specific papers when making claims
        2. Use direct quotes when relevant
        3. Acknowledge if information isn't available in the provided context
        4. Maintain academic tone and precision
        """

    def solve(self, query):
        # Check if search has been performed
        if not os.path.exists("vdb_chunks"):
            st.warning("No papers loaded. Performing search first...")
            search_agent = SearchAgent()
            search_agent.solve(query)
            
        # Load vector store
        vdb_chunks = FAISS.load_local("vdb_chunks", embeddings, index_name="base_and_adjacent", allow_dangerous_deserialization=True)
        
        # Get chat history
        chat_history = st.session_state.get("chat_history", [])
        chat_history_text = "\n".join([f"{sender}: {msg}" for sender, msg in chat_history[-5:]])  # Last 5 messages
        
        # Get relevant chunks
        retrieved = vdb_chunks.as_retriever().get_relevant_documents(query)
        context = "\n".join([doc.page_content for doc in retrieved])
        
        # Generate response
        full_prompt = self.prompt.format(
            chat_history=chat_history_text,
            context=context,
            question=query
        )
        response = self.model.generate_content(full_prompt)
        return response.text

class FutureWorksAgent:
    def __init__(self):
        self.model = model
        self.prompt = """Analyze the current research landscape and identify promising future directions based on the following context and chat history.

        Previous conversation:
        {chat_history}

        Current research context:
        {context}

        Guidelines:
        1. Identify gaps in current research
        2. Suggest specific research directions
        3. Consider technical challenges
        4. Propose methodological improvements
        5. Discuss potential applications

        Focus on concrete, actionable research directions rather than general suggestions.
        """

    def solve(self, query):
        # Check if search has been performed
        if not os.path.exists("vdb_chunks"):
            st.warning("No papers loaded. Performing search first...")
            search_agent = SearchAgent()
            search_agent.solve(query)
            
        # Load vector store
        vdb_chunks = FAISS.load_local("vdb_chunks", embeddings, index_name="base_and_adjacent", allow_dangerous_deserialization=True)
        
        # Get chat history
        chat_history = st.session_state.get("chat_history", [])
        chat_history_text = "\n".join([f"{sender}: {msg}" for sender, msg in chat_history[-5:]])
        
        # Get relevant chunks
        retrieved = vdb_chunks.as_retriever().get_relevant_documents(query)
        context = "\n".join([doc.page_content for doc in retrieved])
        
        # Generate response
        full_prompt = self.prompt.format(
            chat_history=chat_history_text,
            context=context
        )
        response = self.model.generate_content(full_prompt)
        return response.text

class Router:
    def __init__(self):
        self.intent_agent = IntentAgent()
        self.agents = {
            "search": SearchAgent(),
            "qa": QAAgent(),
            "future_works": FutureWorksAgent()
        }
    
    def route_query(self, query):
        st.write("Analyzing query intent...")
        intent = self.intent_agent.get_intent(query)
        
        # Initialize session state if needed
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        agent = self.agents.get(intent)
        st.write(f"Using {intent} agent...")
        
        if agent:
            if intent == "search":
                ans, papers = agent.solve(query)
                return ans, papers
            else:
                return agent.solve(query), None
        else:
            return "Sorry, I couldn't understand your query.", None