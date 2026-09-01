import os
from pathlib import Path


class DocumentReader:
    """
    Reads common document formats and converts them into plain text.

    Supported:
    - PDF
    - DOCX
    - TXT
    """

    def __init__(self):
        pass

    # =====================================
    # MAIN READER
    # =====================================

    def read(self, file_path: str) -> str:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Document not found: {file_path}"
            )

        extension = path.suffix.lower()

        if extension == ".pdf":
            return self.read_pdf(path)

        elif extension == ".docx":
            return self.read_docx(path)

        elif extension == ".txt":
            return self.read_txt(path)

        else:
            raise ValueError(
                f"Unsupported document type: {extension}"
            )

    # =====================================
    # PDF
    # =====================================

    def read_pdf(self, path: Path) -> str:

        try:
            import pypdf
        except ImportError:
            raise ImportError(
                "Install pypdf using: pip install pypdf"
            )

        text_parts = []

        reader = pypdf.PdfReader(
            str(path)
        )

        for page_number, page in enumerate(
            reader.pages,
            start=1
        ):

            text = page.extract_text()

            if text:
                text_parts.append(
                    f"\n[Page {page_number}]\n{text}"
                )

        return "\n".join(
            text_parts
        ).strip()

    # =====================================
    # DOCX
    # =====================================

    def read_docx(self, path: Path) -> str:

        try:
            from docx import Document
        except ImportError:
            raise ImportError(
                "Install python-docx using: "
                "pip install python-docx"
            )

        document = Document(
            str(path)
        )

        paragraphs = []

        for paragraph in document.paragraphs:

            text = paragraph.text.strip()

            if text:
                paragraphs.append(
                    text
                )

        return "\n".join(
            paragraphs
        ).strip()

    # =====================================
    # TXT
    # =====================================

    def read_txt(self, path: Path) -> str:

        encodings = [
            "utf-8",
            "utf-8-sig",
            "cp1252",
            "latin-1"
        ]

        for encoding in encodings:

            try:

                with open(
                    path,
                    "r",
                    encoding=encoding
                ) as file:

                    return file.read().strip()

            except UnicodeDecodeError:
                continue

        raise UnicodeDecodeError(
            "unknown",
            b"",
            0,
            1,
            "Could not decode text file."
        )

    # =====================================
    # CHUNK DOCUMENT
    # =====================================

    def chunk_text(
        self,
        text: str,
        chunk_size: int = 1200,
        overlap: int = 200
    ) -> list:

        text = text.strip()

        if not text:
            return []

        if overlap >= chunk_size:
            raise ValueError(
                "overlap must be smaller than chunk_size"
            )

        chunks = []

        start = 0
        text_length = len(text)

        while start < text_length:

            end = min(
                start + chunk_size,
                text_length
            )

            chunk = text[
                start:end
            ].strip()

            if chunk:
                chunks.append(
                    chunk
                )

            if end >= text_length:
                break

            start = end - overlap

        return chunks

    # =====================================
    # READ + CHUNK
    # =====================================

    def read_and_chunk(
        self,
        file_path: str,
        chunk_size: int = 1200,
        overlap: int = 200
    ) -> list:

        text = self.read(
            file_path
        )

        return self.chunk_text(
            text=text,
            chunk_size=chunk_size,
            overlap=overlap
        )


# =========================================
# SIMPLE FUNCTION
# =========================================

def read_document(
    file_path: str
) -> str:

    reader = DocumentReader()

    return reader.read(
        file_path
    )


# =========================================
# TEST
# =========================================

if __name__ == "__main__":

    file_path = input(
        "Enter document path: "
    ).strip()

    reader = DocumentReader()

    try:

        text = reader.read(
            file_path
        )

        print("\n==============================")
        print("DOCUMENT TEXT")
        print("==============================")

        print(text[:5000])

        chunks = reader.chunk_text(
            text
        )

        print(
            f"\nTotal chunks: {len(chunks)}"
        )

    except Exception as error:

        print(
            f"\n[ERROR] {error}"
        )