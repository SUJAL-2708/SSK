from models.granite import Granite

from memory.vector_db import VectorMemory

from config.settings import (
    MAX_RETRIEVED_MEMORIES,
    MAX_RETRIEVED_DOCUMENTS
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

        decision = (
            self.granite.should_retrieve(
                user_input
            )
        )

        print(
            "\n[RETRIEVAL DECISION]",
            decision
        )

        results = []

        # ---------------------------------
        # PERSONAL MEMORY
        # ---------------------------------

        if decision.get(
            "retrieve_memory",
            False
        ):

            blocks = decision.get(
                "blocks",
                []
            )

            if blocks:

                memories = (
                    self.vector_db.search(
                        query=user_input,
                        blocks=blocks,
                        limit=MAX_RETRIEVED_MEMORIES
                    )
                )

                results.extend(
                    memories
                )

        # ---------------------------------
        # DOCUMENTS
        # ---------------------------------

        if decision.get(
            "retrieve_documents",
            False
        ):

            documents = (
                self.vector_db.search_documents(
                    query=user_input,
                    limit=MAX_RETRIEVED_DOCUMENTS
                )
            )

            results.extend(
                documents
            )

        return results

    # =====================================
    # FORMAT RESULTS
    # =====================================

    def format_results(
        self,
        results: list
    ) -> str:

        if not results:
            return ""

        formatted = []

        for result in results:

            if result.get(
                "type"
            ) == "document":

                formatted.append(
                    (
                        f"[DOCUMENT: "
                        f"{result.get('document_name')}] "
                        f"{result.get('content')}"
                    )
                )

            else:

                formatted.append(
                    (
                        f"[MEMORY: "
                        f"{result.get('block')}] "
                        f"{result.get('content')} "
                        f"(importance: "
                        f"{result.get('importance')})"
                    )
                )

        return "\n".join(
            formatted
        )