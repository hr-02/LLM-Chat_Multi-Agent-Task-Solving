
from config import model
import urllib.request as libreq
import xml.etree.ElementTree as ET
import requests
import os
from langchain.document_loaders import PDFMinerLoader
from langchain_ollama import OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.docstore.in_memory import InMemoryDocstore
import faiss
import streamlit as st


class SearchAgent:
    def __init__(self):
        self.model = model
        self.p = """You are an assistant designed to extract research topics or titles from user queries. 
        When a user asks about a specific topic, identify the central subject of their query and provide 
        a concise, clear title or topic related to that area of research. Focus on the core research concept."""
        
        # Initialize embeddings and index
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.index = faiss.IndexFlatL2(len(self.embeddings.embed_query("hello")))
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=50,
            length_function=len
        )
        
        os.makedirs("papers", exist_ok=True)

    def solve(self, task):
        print(f"Searching for information on: {task}")
        response = self.model.generate_content(self.p + task)
        query = response["content"].strip()

        # Search arXiv
        search_query = "%20".join(query.split())
        url = f'http://export.arxiv.org/api/query?search_query=all:{search_query}&sortBy=relevance&sortOrder=descending&start=0&max_results=5'
        
        with libreq.urlopen(url) as response:
            xml_content = response.read()
        
        root = ET.fromstring(xml_content)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        papers = []
        paper_numbers = []
        
        for entry in root.findall('atom:entry', ns):
            paper_info = {
                'title': entry.find('atom:title', ns).text,
                'link': entry.find('atom:id', ns).text.replace("abs", "pdf"),
                'year': entry.find('atom:published', ns).text[:4]
            }
            
            # Download PDF
            paper_number = os.path.basename(paper_info['link']).strip(".pdf")
            pdf_path = f"papers/{paper_number}.pdf"
            
            try:
                res = requests.get(paper_info['link'])
                with open(pdf_path, 'wb') as f:
                    f.write(res.content)
                paper_numbers.append(paper_number)
                paper_info['paper_number'] = paper_number
                papers.append(paper_info)
            except Exception as e:
                st.warning(f"Failed to download paper: {paper_info['title']}")
                continue

        # Create vector store
        vdb_chunks = FAISS(
            embedding_function=self.embeddings,
            index=self.index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={}
        )
        
        for paper_number in paper_numbers:
            try:
                docs = PDFMinerLoader(f"papers/{paper_number}.pdf").load()
                chunks = self.text_splitter.split_documents(docs)
                vdb_chunks.add_documents(chunks)
            except Exception as e:
                st.warning(f"Error processing paper {paper_number}")
                continue
        
        vdb_chunks.save_local("vdb_chunks", index_name="base_and_adjacent")
        
        return papers, papers