from typing import List, Any
import faiss
import numpy as np
import pickle
import os

class VectorStore:
    def __init__(self, subject: str, data_dir: str = "data/indices"):
        self.subject = subject
        self.index_path = os.path.join(data_dir, f"{subject}.index")
        self.texts_path = os.path.join(data_dir, f"{subject}_texts.pkl")
        self.index = self.load_or_create_index()
        self.texts = self.load_or_create_texts()

    def load_or_create_index(self) -> faiss.Index:
        if os.path.exists(self.index_path):
            return faiss.read_index(self.index_path)
        else:
            # Create a new FAISS index (Flat L2 for simplicity, can be optimized later)
            dimension = 384  # Dimension for 'all-MiniLM-L6-v2' embeddings
            return faiss.IndexFlatL2(dimension)

    def load_or_create_texts(self) -> List[str]:
        if os.path.exists(self.texts_path):
            with open(self.texts_path, 'rb') as f:
                return pickle.load(f)
        else:
            return []

    def search(self, query_vector: np.ndarray, k: int = 5) -> List[Any]:
        D, I = self.index.search(query_vector, k)
        results = [(self.texts[i], D[0][j]) for j, i in enumerate(I[0]) if i < len(self.texts)]
        return results

    def update_index(self, new_vectors: np.ndarray, new_texts: List[str]):
        current_size = self.index.ntotal
        self.index.add(new_vectors)
        self.texts.extend(new_texts)
        self.save_index()
        self.save_texts()

    def save_index(self):
        faiss.write_index(self.index, self.index_path)

    def save_texts(self):
        with open(self.texts_path, 'wb') as f:
            pickle.dump(self.texts, f)