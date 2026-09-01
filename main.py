from input.stt import get_speech_text

from models.qwen import Qwen

from memory.redis import RedisMemory
from memory.consolidation import MemoryConsolidator
from memory.retrieval import MemoryRetriever
from memory.documents import DocumentManager


class SSK:

    def __init__(self):

        print("\nInitializing SSK...")

        # ===============================
        # ACTIVE MEMORY
        # ===============================

        self.redis = RedisMemory()

        # ===============================
        # MEMORY CONSOLIDATION
        # ===============================

        self.consolidator = (
            MemoryConsolidator()
        )

        # ===============================
        # LONG-TERM RETRIEVAL
        # ===============================

        self.retriever = (
            MemoryRetriever()
        )

        # ===============================
        # DOCUMENT SYSTEM
        # ===============================

        self.documents = (
            DocumentManager()
        )

        # ===============================
        # BIG MODEL
        # ===============================

        self.qwen = Qwen()

        print("SSK initialized.")

    # =====================================
    # NORMAL USER MESSAGE
    # =====================================

    def process(
        self,
        user_input: str
    ):

        print(
            f"\nUSER: {user_input}"
        )

        # -------------------------------
        # SAVE TO REDIS
        # -------------------------------

        self.redis.add_message(
            role="user",
            content=user_input
        )

        # -------------------------------
        # RETRIEVE LONG-TERM MEMORY
        # -------------------------------

        retrieved = (
            self.retriever.retrieve(
                user_input
            )
        )

        retrieved_context = (
            self.retriever.format_results(
                retrieved
            )
        )

        # -------------------------------
        # ACTIVE REDIS MEMORY
        # -------------------------------

        active_memory = (
            self.redis.formatted()
        )

        # -------------------------------
        # QWEN RESPONSE
        # -------------------------------

        response = self.qwen.generate(
            user_input=user_input,
            active_memory=active_memory,
            retrieved_memory=retrieved_context
        )

        print(
            f"\nSSK: {response}"
        )

        # -------------------------------
        # SAVE RESPONSE TO REDIS
        # -------------------------------

        self.redis.add_message(
            role="assistant",
            content=response
        )

        # -------------------------------
        # MEMORY CONSOLIDATION
        # -------------------------------

        if self.redis.limit_reached():

            print(
                "\n[MEMORY] "
                "10-message limit reached."
            )

            self.consolidator.consolidate()

        return response

    # =====================================
    # DOCUMENT
    # =====================================

    def add_document(
        self,
        file_path: str
    ):

        print(
            "\n[DOCUMENT] Reading document..."
        )

        result = (
            self.documents.add_document(
                file_path
            )
        )

        print(
            "\n[DOCUMENT] Successfully added."
        )

        print(
            f"Name    : "
            f"{result['document_name']}"
        )

        print(
            f"Type    : "
            f"{result['file_type']}"
        )

        print(
            f"Chunks  : "
            f"{result['chunks']}"
        )

        return result


# =========================================
# MAIN
# =========================================

if __name__ == "__main__":

    ssk = SSK()

    print(
        "\n=============================="
    )

    print(
        "             SSK"
    )

    print(
        "=============================="
    )

    print(
        "\nChoose input mode:"
    )

    print(
        "1. Voice"
    )

    print(
        "2. Text"
    )

    print(
        "3. Add Document"
    )

    mode = input(
        "\nEnter 1, 2 or 3: "
    ).strip()

    # =====================================
    # VOICE MODE
    # =====================================

    if mode == "1":

        print(
            "\n=============================="
        )

        print(
            "        SSK VOICE MODE"
        )

        print(
            "=============================="
        )

        while True:

            try:

                user_input = (
                    get_speech_text()
                )

            except Exception as error:

                print(
                    f"\n[STT ERROR] {error}"
                )

                break

            if not user_input:
                continue

            print(
                f"\nYou: {user_input}"
            )

            if user_input.lower() == "exit":
                break

            ssk.process(
                user_input
            )

    # =====================================
    # TEXT MODE
    # =====================================

    elif mode == "2":

        print(
            "\n=============================="
        )

        print(
            "        SSK TEXT MODE"
        )

        print(
            "=============================="
        )

        print(
            "\nType your message."
        )

        print(
            "Type 'exit' to stop."
        )

        print(
            "Use '/document <path>' "
            "to add a document."
        )

        while True:

            user_input = input(
                "\nYou: "
            ).strip()

            if not user_input:
                continue

            if user_input.lower() == "exit":
                break

            # ---------------------------
            # DOCUMENT COMMAND
            # ---------------------------

            if user_input.lower().startswith(
                "/document "
            ):

                file_path = user_input[
                    len("/document "):
                ].strip()

                try:

                    ssk.add_document(
                        file_path
                    )

                except Exception as error:

                    print(
                        f"\n[DOCUMENT ERROR] "
                        f"{error}"
                    )

                continue

            # ---------------------------
            # NORMAL CHAT
            # ---------------------------

            ssk.process(
                user_input
            )

    # =====================================
    # DOCUMENT MODE
    # =====================================

    elif mode == "3":

        print(
            "\n=============================="
        )

        print(
            "       DOCUMENT MODE"
        )

        print(
            "=============================="
        )

        file_path = input(
            "\nEnter document path: "
        ).strip()

        if file_path:

            try:

                ssk.add_document(
                    file_path
                )

            except Exception as error:

                print(
                    f"\n[DOCUMENT ERROR] "
                    f"{error}"
                )

    else:

        print(
            "\nInvalid option."
        )