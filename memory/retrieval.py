from models.granite import Granite
from memory.vector_db import VectorMemory

from config.settings import (
    MAX_RETRIEVED_MEMORIES
)


class MemoryRetriever:

    def __init__(self):

        self.granite = Granite()

        self.vector_db = VectorMemory()

    # =====================================
    # RETRIEVE
    # =====================================

    def retrieve(
        self,
        user_input: str
    ) -> list:

        # -------------------------------
        # STEP 1
        # ASK GRANITE
        # -------------------------------

        decision = self.granite.should_retrieve(
            user_input
        )

        print(
            "\n[RETRIEVAL DECISION]",
            decision
        )

        if not decision.get(
            "retrieve",
            False
        ):

            return []

        blocks = decision.get(
            "blocks",
            []
        )

        if not blocks:
            return []

        # -------------------------------
        # STEP 2
        # VECTOR SEARCH
        # -------------------------------

        results = self.vector_db.search(
            query=user_input,
            blocks=blocks,
            limit=MAX_RETRIEVED_MEMORIES
        )

        return results

    # =====================================
    # FORMAT
    # =====================================

    def format_results(
        self,
        results: list
    ) -> str:

        if not results:
            return ""

        return "\n".join(
            [
                (
                    f"[{result['block']}] "
                    f"{result['content']} "
                    f"(importance: "
                    f"{result['importance']})"
                )
                for result in results
            ]
        )