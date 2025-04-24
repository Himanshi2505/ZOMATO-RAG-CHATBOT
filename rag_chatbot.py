import numpy as np
import json
import faiss
import re
from sentence_transformers import SentenceTransformer
from transformers import pipeline

class RestaurantRAG:
    def __init__(self):
        # Load knowledge base components
        with open('knowledge_base/documents.json', 'r') as f:
            self.documents = json.load(f)
        self.embeddings = np.load('knowledge_base/embeddings.npy')
        self.index = faiss.read_index('knowledge_base/faiss_index.bin')
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.generator = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",
            device_map="auto"
        )

        self.conversation_history = []

    def _retrieve(self, query, top_k=5):
        query_embedding = self.embedder.encode([query])
        distances, indices = self.index.search(query_embedding, top_k)
        results = []
        for idx in indices[0]:
            doc = self.documents[idx]
            results.append(doc["content"])
        return results

    def query(self, question):
        # Retrieve relevant context
        context_docs = self._retrieve(question, top_k=5)
        context = "\n\n".join(context_docs)
        prompt = (
            f"Context: {context}\n\n"
            f"Question: {question}\n"
            f"Answer:"
        )

        response = self.generator(
            prompt,
            max_length=256,
            num_return_sequences=1,
            temperature=0.3
        )[0]['generated_text']
        answer = response.strip().split("Answer:")[-1].strip()
        self.conversation_history.append((question, answer))
        return answer


