from typing import List, Dict
import ollama

class QwenModel:
    def __init__(self, model_name: str = "qwen:2.5"):
        self.model_name = model_name
        self.client = ollama.Client()
        
    def generate_content(self, prompt: str) -> str:
        """Generate content using Qwen model"""
        try:
            response = self.client.chat(
                model=self.model_name,
                messages=[{
                    'role': 'user',
                    'content': prompt
                }]
            )
            return response['message']
        except Exception as e:
            return f"Error generating content: {str(e)}"

model = QwenModel()

