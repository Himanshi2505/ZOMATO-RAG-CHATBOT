import os
import json
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import faiss

def load_documents():
    """Load document chunks from JSON file"""
    with open('knowledge_base/documents.json', 'r', encoding='utf-8') as f:
        documents = json.load(f)
    return documents

def create_embeddings(documents):
    """Create embeddings for documents using a sentence transformer model"""
    # Load model
    print("Loading model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Extract content from documents
    texts = [doc["content"] for doc in documents]
    
    # Generate embeddings
    print("Generating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True)
    
    return embeddings

def build_faiss_index(embeddings):
    """Build a FAISS index for fast similarity search"""
    # Create FAISS index
    print("Building FAISS index...")
    dimension = embeddings.shape[1]  # Get the dimension of embeddings
    index = faiss.IndexFlatL2(dimension)  # L2 distance (Euclidean)
    
    # Add vectors to index
    index.add(np.array(embeddings).astype('float32'))
    
    return index

def main():
    # Create directories if they don't exist
    os.makedirs('knowledge_base', exist_ok=True)
    
    # Load documents
    print("Loading documents...")
    documents = load_documents()
    
    if not documents:
        print("No documents found. Run build_knowledge_base.py first.")
        return
    
    # Create embeddings
    embeddings = create_embeddings(documents)
    
    # Save embeddings
    print("Saving embeddings...")
    np.save('knowledge_base/embeddings.npy', embeddings)
    
    # Build FAISS index
    index = build_faiss_index(embeddings)
    
    # Save index
    print("Saving FAISS index...")
    faiss.write_index(index, 'knowledge_base/faiss_index.bin')
    
    print(f"Embeddings and index created successfully for {len(documents)} documents.")
    print("Files saved to knowledge_base/embeddings.npy and knowledge_base/faiss_index.bin")

if __name__ == "__main__":
    main()
