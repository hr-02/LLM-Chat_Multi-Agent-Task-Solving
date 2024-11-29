from config import model
from agents import SearchAgent, QAAgent, FutureWorksAgent
import streamlit as st

class ChooseAgent:
    def __init__(self):
        self.model = model
        self.prompt = """You are an intention classifier for a research paper assistant. Given a user query, classify it into one of these categories:
        - "search": User wants to find relevant research papers on a topic
        - "qa": User has questions about specific papers or content
        - "future_works": User wants to know about future research directions, review combination of multiple papers, generate new ideas etc.
        
        Example queries and their intents:
        "Find papers about machine learning" -> "search"
        "What does the paper say about the methodology?" -> "qa"
        "What are the future research directions in this field?" -> "future_works"
        
        Respond with just the chosen category.
        
        Query: {query}"""
    
    def get_choice(self, query):
        response = self.model.generate_content(self.prompt.format(query=query))
        return response['content'].strip().lower()

class Master:
    def __init__(self):
        self.choose_agent = ChooseAgent()
        self.agents = {
            "search": SearchAgent(),
            "qa": QAAgent(),
            "future_works": FutureWorksAgent()
        }
    
    def route_query(self, query):
        st.write(f"Analyzing query to choose agent...")
        choice = self.choose_agent.get_choice(query)
        agent = self.agents.get(choice)
        st.write(f"Using {choice} agent...")
        
        if agent:
            if choice == "search":
                ans, d = agent.solve(query)
                return ans, d
            return agent.solve(query), None
        else:
            return "Unknown Query", None