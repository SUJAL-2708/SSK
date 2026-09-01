from typing import Any
from unittest import result

import chromadb
import ollama

from config.settings import (
    CHROMA_PATH,
    CHROMA_COLLECTION_PREFIX,
    EMBEDDING_MODEL,
    OLLAMA_HOST
)


class VectorMemory:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path=CHROMA_PATH
        )

        self.ollama = ollama.Client(
            host=OLLAMA_HOST
        )

    # =====================================
    # COLLECTION
    # =====================================

    def _collection_name(
        self,
        block: str
    ) -> str:

        return (
            f"{CHROMA_COLLECTION_PREFIX}"
            f"{block}"
        )

    def _get_collection(
        self,
        block: str
    ):

        return self.client.get_or_create_collection(
            name=self._collection_name(block)
        )

    # =====================================
    # EMBEDDING
    # =====================================

    def embed(
        self,
        text: str
    ) -> list:

        response = self.ollama.embed(
            model=EMBEDDING_MODEL,
            input=text
        )

        return response["embeddings"][0]

    # =====================================
    # SAVE
    # =====================================

    def save_memory(
        self,
        memory_id: str,
        block: str,
        content: str,
        importance: int
    ):

        collection = self._get_collection(
            block
        )

        embedding = self.embed(
            content
        )

        collection.upsert(
            ids=[memory_id],

            documents=[content],

            embeddings=[embedding],

            metadatas=[
                {
                    "memory_id": memory_id,
                    "block": block,
                    "importance": importance
                }
            ]
        )

    # =====================================
    # SEARCH
    # =====================================

    def search(
        self,
        query: str,
        blocks: list,
        limit: int = 5
    ) -> list:

        query_embedding = self.embed(
            query
        )

        results = []

        for block in blocks:

            collection = self._get_collection(
                block
            )

            if collection.count() == 0:
                continue

            result = collection.query(
                query_embeddings=[
                    query_embedding
                ],

                n_results=min(
                    limit,
                    collection.count()
                )
            )

            documents = result["documents"]
            metadatas = result["metadatas"]
            distances = result["distances"]

            if documents is None or metadatas is None or distances is None:
                continue

            documents = documents[0]
            metadatas = metadatas[0]
            distances = distances[0]

            for document, metadata, distance in zip(
                documents,
                metadatas,
                distances
            ):

                results.append(
                    {
                        "content": document,
                        "memory_id": metadata.get(
                            "memory_id"
                        ),
                        "block": metadata.get(
                            "block"
                        ),
                        "importance": metadata.get(
                            "importance",
                            0
                        ),
                        "distance": distance
                    }
                )

        results.sort(
            key=lambda x: x["distance"]
        )

        return results[:limit]