import os

from dotenv import load_dotenv

load_dotenv()


# =========================
# OLLAMA
# =========================

OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434"
)

SMALL_MODEL = "granite4.1:3b"

BIG_MODEL = "qwen3:8b"

EMBEDDING_MODEL = "qwen3-embedding:4b"


# =========================
# REDIS
# =========================

REDIS_HOST = os.getenv(
    "REDIS_HOST",
    "localhost"
)

REDIS_PORT = int(
    os.getenv(
        "REDIS_PORT",
        "6379"
    )
)

REDIS_DB = int(
    os.getenv(
        "REDIS_DB",
        "0"
    )
)

REDIS_KEY = "ssk:conversation"

MESSAGE_LIMIT = 10


# =========================
# MYSQL
# =========================

MYSQL_HOST = os.getenv(
    "MYSQL_HOST",
    "localhost"
)

MYSQL_PORT = int(
    os.getenv(
        "MYSQL_PORT",
        "3306"
    )
)

MYSQL_USER = os.getenv(
    "MYSQL_USER",
    "root"
)

MYSQL_PASSWORD = os.getenv(
    "MYSQL_PASSWORD",
    ""
)

MYSQL_DATABASE = os.getenv(
    "MYSQL_DATABASE",
    "ssk_memory"
)


# =========================
# CHROMA
# =========================

CHROMA_PATH = os.getenv(
    "CHROMA_PATH",
    "./data/chroma"
)

CHROMA_COLLECTION_PREFIX = "ssk_"


# =========================
# PERSONAL MEMORY BLOCKS
# =========================

MEMORY_BLOCKS = [
    "user",
    "project",
    "hobby",
    "academics",
    "work",
    "other"
]


# =========================
# DOCUMENT SETTINGS
# =========================

DOCUMENT_COLLECTION = "ssk_documents"

DOCUMENT_CHUNK_SIZE = 1200

DOCUMENT_CHUNK_OVERLAP = 200


# =========================
# MEMORY SETTINGS
# =========================

MIN_IMPORTANCE_TO_SAVE = 4

MAX_RETRIEVED_MEMORIES = 5

MAX_RETRIEVED_DOCUMENTS = 5