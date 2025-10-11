from typing import List, Dict, Any

# Define a type for the chatbot query response
class ChatbotResponse:
    def __init__(self, answer: str, context: str, sources: List[str]):
        self.answer = answer
        self.context = context
        self.sources = sources

# Define a type for the subject
class Subject:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

# Define a type for the request to the chatbot
class ChatbotQuery:
    def __init__(self, question: str, subject: str):
        self.question = question
        self.subject = subject

# Define a type for the background job status
class JobStatus:
    def __init__(self, job_id: str, status: str, result: Any = None):
        self.job_id = job_id
        self.status = status
        self.result = result

# Define a type for the embedding response
class EmbeddingResponse:
    def __init__(self, embeddings: List[float]):
        self.embeddings = embeddings