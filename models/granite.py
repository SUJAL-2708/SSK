import json
import re
import ollama

from config.settings import (
    OLLAMA_HOST,
    SMALL_MODEL
)


class Granite:
    """
    Interface for Granite 4.1 3B.

    Granite is responsible for:
    - summarization
    - memory decisions
    - memory classification
    - retrieval decisions
    """

    def __init__(self):
        self.client = ollama.Client(
            host=OLLAMA_HOST
        )

        self.model = SMALL_MODEL

    def generate(self, prompt: str) -> str:
        """
        Generate a normal text response.
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

    def generate_json(self, prompt: str) -> dict:
        """
        Ask Granite for JSON and safely parse it.
        """

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            format="json"
        )

        content = response["message"]["content"]

        try:
            return json.loads(content)

        except json.JSONDecodeError:

            # Try extracting JSON from accidental markdown
            match = re.search(
                r"\{.*\}",
                content,
                re.DOTALL
            )

            if match:
                return json.loads(
                    match.group()
                )

            raise ValueError(
                f"Granite returned invalid JSON:\n{content}"
            )

    # =====================================
    # SUMMARIZATION
    # =====================================

    def summarize(self, conversation: str) -> str:

        prompt = f"""
You are the memory summarization component of an AI assistant.

Summarize the following conversation.

Keep:
- important facts
- decisions
- user preferences
- projects
- academic information
- work information
- hobbies
- future plans
- important events

Do NOT include:
- meaningless small talk
- repeated information
- greetings
- filler

Conversation:

{conversation}

Return only the summary.
"""

        return self.generate(prompt)

    # =====================================
    # MEMORY DECISION
    # =====================================

    def should_retrieve(self, user_input: str) -> dict:

        prompt = f"""
You are the memory retrieval decision system.

Determine whether the AI assistant needs long-term memory
to answer the user's current message.

Current user message:

{user_input}

Available memory blocks:

- user
- project
- hobby
- academics
- work
- other

Return JSON exactly like:

{{
    "retrieve": true,
    "blocks": ["project"],
    "reason": "short explanation"
}}

If long-term memory is NOT required:

{{
    "retrieve": false,
    "blocks": [],
    "reason": "short explanation"
}}

Only retrieve memory when it can meaningfully improve the answer.
"""

        result = self.generate_json(prompt)

        result.setdefault("retrieve", False)
        result.setdefault("blocks", [])
        result.setdefault("reason", "")

        return result

    # =====================================
    # MEMORY EXTRACTION
    # =====================================

    def extract_memories(self, summary: str) -> list:

        prompt = f"""
You are the long-term memory extraction system.

From the following conversation summary, identify information
that is genuinely useful to remember about the user.

Do NOT save:
- temporary statements
- greetings
- normal conversation
- random facts with no future usefulness
- one-time requests

Potential memories:

{summary}

Return JSON exactly like:

{{
    "memories": [
        {{
            "content": "memory content",
            "importance": 7
        }}
    ]
}}

Importance:
1-3 = unimportant
4-6 = useful
7-8 = important
9-10 = extremely important

Return an empty list if nothing should be remembered.
"""

        result = self.generate_json(prompt)

        return result.get(
            "memories",
            []
        )

    # =====================================
    # MEMORY CLASSIFICATION
    # =====================================

    def classify_memory(self, content: str) -> dict:

        prompt = f"""
Classify this memory into exactly ONE category.

Memory:

{content}

Categories:

user
project
hobby
academics
work
other

Return JSON:

{{
    "block": "project"
}}

Return only one category.
"""

        result = self.generate_json(prompt)

        block = result.get(
            "block",
            "other"
        ).lower().strip()

        allowed = {
            "user",
            "project",
            "hobby",
            "academics",
            "work",
            "other"
        }

        if block not in allowed:
            block = "other"

        return {
            "block": block
        }