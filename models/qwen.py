import ollama

from config.settings import (
    OLLAMA_HOST,
    BIG_MODEL
)


class Qwen:
    """
    Interface for Qwen 3 8B.

    Qwen is responsible for generating
    the final response to the user.
    """

    def __init__(self):

        self.client = ollama.Client(
            host=OLLAMA_HOST
        )

        self.model = BIG_MODEL

    def generate(
        self,
        user_input: str,
        active_memory: str = "",
        retrieved_memory: str = ""
    ) -> str:

        prompt = f"""
You are SSK, a personal AI assistant.

Answer the user's current request naturally and accurately.

You have access to two types of context:

1. ACTIVE MEMORY
Recent conversation currently held in Redis.

2. RETRIEVED LONG-TERM MEMORY
Relevant memories retrieved from SSK's long-term memory system.

Use memory only when it is relevant.

Do not mention:
- Redis
- MySQL
- Vector DB
- Granite
- Qwen
- memory retrieval systems

to the user.

========================
ACTIVE MEMORY
========================

{active_memory}

========================
RETRIEVED MEMORY
========================

{retrieved_memory}

========================
CURRENT USER MESSAGE
========================

{user_input}

Answer the user directly.
"""

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]