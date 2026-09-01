import chromadb
import ollama

from config.settings import (
    CHROMA_PATH,
    CHROMA_COLLECTION_PREFIX,
    DOCUMENT_COLLECTION,
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
    # PERSONAL MEMORY COLLECTION
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
            name=self._collection_name(
                block
            )
        )

    # =====================================
    # DOCUMENT COLLECTION
    # =====================================

    def _get_document_collection(self):

        return self.client.get_or_create_collection(
            name=DOCUMENT_COLLECTION
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
    # SAVE PERSONAL MEMORY
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
                    "importance": importance,
                    "type": "memory"
                }
            ]
        )

    # =====================================
    # SAVE DOCUMENT CHUNK
    # =====================================

    def save_document_chunk(
        self,
        document_id: str,
        chunk_id: str,
        document_name: str,
        content: str,
        chunk_index: int
    ):

        collection = (
            self._get_document_collection()
        )

        embedding = self.embed(
            content
        )

        vector_id = (
            f"{document_id}_{chunk_id}"
        )

        collection.upsert(
            ids=[vector_id],

            documents=[content],

            embeddings=[embedding],

            metadatas=[
                {
                    "document_id": document_id,
                    "document_name": document_name,
                    "chunk_index": chunk_index,
                    "type": "document"
                }
            ]
        )

    # =====================================
    # SEARCH PERSONAL MEMORY
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

            if (
                not documents
                or not metadatas
                or not distances
            ):
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
                        "distance": distance,
                        "type": "memory"
                    }
                )

        results.sort(
            key=lambda x: x["distance"]
        )

        return results[:limit]

    # =====================================
    # SEARCH DOCUMENTS
    # =====================================

    def search_documents(
        self,
        query: str,
        limit: int = 5
    ) -> list:

        collection = (
            self._get_document_collection()
        )

        if collection.count() == 0:
            return []

        query_embedding = self.embed(
            query
        )

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

        if (
            not documents
            or not metadatas
            or not distances
        ):
            return []

        documents = documents[0]
        metadatas = metadatas[0]
        distances = distances[0]

        results = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):

            results.append(
                {
                    "content": document,
                    "document_id": metadata.get(
                        "document_id"
                    ),
                    "document_name": metadata.get(
                        "document_name"
                    ),
                    "chunk_index": metadata.get(
                        "chunk_index"
                    ),
                    "distance": distance,
                    "type": "document"
                }
            )

        return results