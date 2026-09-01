from input.stt import get_speech_text

from models.qwen import Qwen

from memory.redis import RedisMemory
from memory.consolidation import MemoryConsolidator
from memory.retrieval import MemoryRetriever


class SSK:

    def __init__(self):

        print("Initializing SSK...")

        # ---------------------------------
        # ACTIVE MEMORY
        # ---------------------------------

        self.redis = RedisMemory()

        # ---------------------------------
        # MEMORY CONSOLIDATION
        # ---------------------------------

        self.consolidator = MemoryConsolidator()

        # ---------------------------------
        # LONG-TERM MEMORY RETRIEVAL
        # ---------------------------------

        self.retriever = MemoryRetriever()

        # ---------------------------------
        # BIG LANGUAGE MODEL
        # ---------------------------------

        self.qwen = Qwen()

        print("SSK initialized.")

    # =====================================
    # PROCESS USER INPUT
    # =====================================

    def process(
        self,
        user_input: str
    ):

        if not user_input:
            return None

        print(
            f"\nUSER: {user_input}"
        )

        # ---------------------------------
        # SAVE USER MESSAGE TO REDIS
        # ---------------------------------

        self.redis.add_message(
            role="user",
            content=user_input
        )

        # ---------------------------------
        # CHECK LONG-TERM MEMORY
        # ---------------------------------

        retrieved = self.retriever.retrieve(
            user_input
        )

        retrieved_context = (
            self.retriever.format_results(
                retrieved
            )
        )

        # ---------------------------------
        # GET CURRENT ACTIVE MEMORY
        # ---------------------------------

        active_memory = (
            self.redis.formatted()
        )

        # ---------------------------------
        # SEND EVERYTHING TO QWEN
        # ---------------------------------

        response = self.qwen.generate(
            user_input=user_input,
            active_memory=active_memory,
            retrieved_memory=retrieved_context
        )

        # ---------------------------------
        # DISPLAY RESPONSE
        # ---------------------------------

        print(
            f"\nSSK: {response}"
        )

        # ---------------------------------
        # SAVE ASSISTANT RESPONSE TO REDIS
        # ---------------------------------

        self.redis.add_message(
            role="assistant",
            content=response
        )

        # ---------------------------------
        # CHECK 10-MESSAGE MEMORY CYCLE
        # ---------------------------------

        if self.redis.limit_reached():

            print(
                "\n[MEMORY] "
                "10-message limit reached."
            )

            self.consolidator.consolidate()

        return response


# =========================================
# VOICE MODE
# =========================================

def voice_mode(ssk):

    print("\n==============================")
    print("       SSK VOICE MODE")
    print("==============================")

    print("\nSpeak into your microphone.")
    print("Press Ctrl+C to stop.\n")

    while True:

        try:

            # -----------------------------
            # MICROPHONE → STT → TEXT
            # -----------------------------

            user_input = get_speech_text()

            if not user_input:
                print(
                    "[STT] No speech detected."
                )
                continue

            # -----------------------------
            # SEND TEXT TO SSK
            # -----------------------------

            ssk.process(
                user_input
            )

        except KeyboardInterrupt:

            print(
                "\n\n[SSK] Voice mode stopped."
            )

            break

        except Exception as error:

            print(
                f"\n[ERROR] {error}"
            )

            print(
                "[SSK] Trying again...\n"
            )


# =========================================
# TEXT MODE
# =========================================

def text_mode(ssk):

    print("\n==============================")
    print("        SSK TEXT MODE")
    print("==============================")

    print(
        "\nType your message."
    )

    print(
        "Type 'exit' to stop.\n"
    )

    while True:

        try:

            user_input = input(
                "You: "
            ).strip()

            if user_input.lower() == "exit":
                break

            if not user_input:
                continue

            ssk.process(
                user_input
            )

        except KeyboardInterrupt:

            print(
                "\n\n[SSK] Text mode stopped."
            )

            break

        except Exception as error:

            print(
                f"\n[ERROR] {error}\n"
            )


# =========================================
# MAIN
# =========================================

if __name__ == "__main__":

    ssk = SSK()

    print("\n==============================")
    print("            SSK")
    print("==============================")

    print("\nChoose input mode:")
    print("1. Voice")
    print("2. Text")

    while True:

        choice = input(
            "\nEnter 1 or 2: "
        ).strip()

        if choice == "1":

            voice_mode(ssk)
            break

        elif choice == "2":

            text_mode(ssk)
            break

        else:

            print(
                "Please enter 1 or 2."
            )