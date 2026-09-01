import uuid
from pathlib import Path

from input.document_reader import DocumentReader

from memory.mysql import MySQLMemory
from memory.vector_db import VectorMemory


class DocumentManager:

    def __init__(self):

        self.reader = DocumentReader()

        self.mysql = MySQLMemory()

        self.vector_db = VectorMemory()

    # =====================================
    # ADD DOCUMENT
    # =====================================

    def add_document(
        self,
        file_path: str
    ):

        path = Path(file_path)

        if not path.exists():

            raise FileNotFoundError(
                f"Document not found: {file_path}"
            )

        print(
            f"\n[DOCUMENT] Reading: "
            f"{path.name}"
        )

        # ---------------------------------
        # READ + CHUNK
        # ---------------------------------

        chunks = self.reader.read_and_chunk(
            file_path=file_path
        )

        if not chunks:

            raise ValueError(
                "No readable text found "
                "in the document."
            )

        # ---------------------------------
        # DOCUMENT ID
        # ---------------------------------

        document_id = str(
            uuid.uuid4()
        )

        file_type = (
            path.suffix.lower()
            .replace(".", "")
        )

        # ---------------------------------
        # MYSQL DOCUMENT
        # ---------------------------------

        self.mysql.save_document(
            document_id=document_id,
            document_name=path.name,
            file_type=file_type
        )

        # ---------------------------------
        # SAVE CHUNKS
        # ---------------------------------

        for index, chunk in enumerate(
            chunks
        ):

            chunk_id = str(
                uuid.uuid4()
            )

            # MySQL
            self.mysql.save_document_chunk(
                chunk_id=chunk_id,
                document_id=document_id,
                chunk_index=index,
                content=chunk
            )

            # Chroma
            self.vector_db.save_document_chunk(
                document_id=document_id,
                chunk_id=chunk_id,
                document_name=path.name,
                content=chunk,
                chunk_index=index
            )

        print(
            f"[DOCUMENT] Saved "
            f"{len(chunks)} chunks."
        )

        return {
            "document_id": document_id,
            "document_name": path.name,
            "file_type": file_type,
            "chunks": len(chunks)
        }