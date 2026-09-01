import uuid

from models.granite import Granite
from memory.classifier import MemoryClassifier
from memory.mysql import MySQLMemory
from memory.vector_db import VectorMemory
from memory.redis import RedisMemory

from config.settings import (
    MIN_IMPORTANCE_TO_SAVE
)


class MemoryConsolidator:

    def __init__(self):

        self.granite = Granite()

        self.classifier = MemoryClassifier()

        self.redis = RedisMemory()

        self.mysql = MySQLMemory()

        self.vector_db = VectorMemory()

    # =====================================
    # CONSOLIDATE
    # =====================================

    def consolidate(self):

        messages = self.redis.get_messages()

        if not messages:
            return []

        conversation = "\n".join(
            f"{message['role'].upper()}: "
            f"{message['content']}"
            for message in messages
        )

        # -------------------------------
        # STEP 1
        # SUMMARY
        # -------------------------------

        summary = self.granite.summarize(
            conversation
        )

        print("\n[MEMORY] Summary:")
        print(summary)

        # -------------------------------
        # STEP 2
        # EXTRACT
        # -------------------------------

        memories = self.granite.extract_memories(
            summary
        )

        saved_memories = []

        # -------------------------------
        # STEP 3
        # PROCESS
        # -------------------------------

        for memory in memories:

            content = memory.get(
                "content",
                ""
            ).strip()

            importance = int(
                memory.get(
                    "importance",
                    0
                )
            )

            if not content:
                continue

            if importance < MIN_IMPORTANCE_TO_SAVE:
                continue

            # ---------------------------
            # CLASSIFY
            # ---------------------------

            block = self.classifier.classify(
                content
            )

            # ---------------------------
            # CREATE ID
            # ---------------------------

            memory_id = str(
                uuid.uuid4()
            )

            # ---------------------------
            # MYSQL
            # ---------------------------

            self.mysql.save_memory(
                memory_id=memory_id,
                block=block,
                content=content,
                importance=importance
            )

            # ---------------------------
            # VECTOR DB
            # ---------------------------

            self.vector_db.save_memory(
                memory_id=memory_id,
                block=block,
                content=content,
                importance=importance
            )

            saved_memories.append(
                {
                    "memory_id": memory_id,
                    "block": block,
                    "content": content,
                    "importance": importance
                }
            )

        # -------------------------------
        # STEP 4
        # START NEW REDIS CYCLE
        # -------------------------------

        self.redis.clear()

        print(
            f"\n[MEMORY] Saved "
            f"{len(saved_memories)} memories."
        )

        return saved_memories