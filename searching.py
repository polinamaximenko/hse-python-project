from typing import Any, Dict, List

import numpy as np
import pandas as pd
from datasets import Dataset
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter


class SemanticSearch:
    def __init__(self, text, query, model = 'ai-forever/ru-en-RoSBERTa'):
        """Инициализация модели для создания эмбеддингов."""
        self.text = text
        self.model = SentenceTransformer(model)
        self.chunks = self.chunk_text()
        self.df = self.embed_chunks()
        self.query = query
        self.question_embedding = self.embed_query(query)
        self.embeddings_dataset = self.initialize_index()
        self.results = self.search()

    def chunk_text(self, chunk_size: int = 500, 
                   chunk_overlap: int = 30) -> Dict[str, List[Dict]]:
        """Разбиене текста документа на чанки."""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

        chunks = []
        text_chunks = splitter.split_text(self.text)
        for i, chunk in enumerate(text_chunks):
            chunk_data = {
                'text': chunk,
                'chunk_info': {
                    'position': i,
                    'total_chunks': len(text_chunks),
                    'size_chars': len(chunk),
                }
            }
            chunks.append(chunk_data)

        return chunks

    def embed_chunks(self) -> pd.DataFrame:
        """Преобразование чанков документа в эмбеддинги."""
        df = pd.DataFrame(self.chunks)
        embeddings = self.model.encode(
            df["text"].tolist(),
            prompt_name="search_document",
            show_progress_bar=True
        )
        df["embeddings"] = list(embeddings)
        return df
    
    def initialize_index(self): 
        """Создание FAISS-индексов для семантического поиска."""
        embeddings_dataset = Dataset.from_pandas(self.df)
        embeddings_dataset.add_faiss_index(column="embeddings")
        return embeddings_dataset

    def embed_query(self, query: str) -> List[float]:
        """Преобразование поискового запроса в эмбеддинг."""
        return self.model.encode(query, prompt_name="search_query")

    def search(
        self,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """Возвращает top_k наиболее релевантных чанков документа."""

        if isinstance(self.question_embedding, np.ndarray) and self.question_embedding.size == 0:
            raise ValueError("Пустой эмбеддинг запроса")

        if "embeddings" not in self.embeddings_dataset._indexes:
            raise ValueError("FAISS-индекс не инициализирован")

        query_vector = np.array(self.question_embedding, dtype="float32")

        scores, samples = self.embeddings_dataset.get_nearest_examples(
            "embeddings",
            query_vector,
            k=top_k,
        )

        results = []
        for score, text, info in zip(
            scores,
            samples["text"],
            samples["chunk_info"],
        ):
            results.append(
                {
                    "text": text,
                    "score": float(score),
                    "position": info["position"],
                    "chunk_size": info["size_chars"],
                }
            )

        return results
    
    def context_preparation(self) -> str:
        """Подготовка контекста из результатов поиска для передачи в модель ответа."""
        context_parts = []
        for res in self.results:
            context_parts.append(res["text"])
        return "\n\n".join(context_parts)
    

if __name__ == "__main__":
    pass
