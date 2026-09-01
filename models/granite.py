import json
import ollama

from config.settings import (
    OLLAMA_HOST,
    SMALL_MODEL
)


class Granite:

    def __init__(self):

        self.client = ollama.Client(
            host=OLLAMA_HOST
        )

        self.model = SMALL_MODEL

    # =====================================
    # GENERATE JSON
    # =====================================

    def generate_json(
        self,
        prompt: str
    ) -> dict:

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0
            }
        )

        content = response["message"]["content"].strip()

        # Remove markdown JSON fences if Granite
        # happens to return them.

        if content.startswith("```"):

            content = content.replace(
                "```json",
                ""
            )

            content = content.replace(
                "```",
                ""
            )

            content = content.strip()

        try:

            return json.loads(
                content
            )

        except json.JSONDecodeError:

            print(
                "\n[GRANITE ERROR] "
                "Invalid JSON returned."
            )

            print(
                "Granite output:"
            )

            print(content)

            return {
                "retrieve_memory": False,
                "retrieve_documents": False,
                "blocks": [],
                "reason": "Granite returned invalid JSON."
            }

    # =====================================
    # RETRIEVAL DECISION
    # =====================================

    def should_retrieve(
        self,
        user_input: str
    ) -> dict:

        prompt = f"""
You are the memory and document retrieval
decision system of SSK.

Your job is to decide whether SSK needs
long-term personal memory or uploaded
documents to answer the user's current
message.

CURRENT USER MESSAGE:
{user_input}

PERSONAL MEMORY CATEGORIES:

- user
- project
- hobby
- academics
- work
- other

AVAILABLE RETRIEVAL SOURCES:

1. Personal memory
2. Uploaded documents
3. Both
4. Neither

RULES:

- Use personal memory when the question
  depends on information about the user,
  their projects, hobbies, academics,
  work, or other saved personal information.

- Use uploaded documents when the user
  asks about information that may exist
  inside an uploaded document.

- Use both when both personal memory and
  uploaded documents can help.

- Use neither when the current message
  can be answered without long-term
  information.

Return ONLY valid JSON.

FORMAT:

{{
    "retrieve_memory": true,
    "retrieve_documents": false,
    "blocks": ["project"],
    "reason": "short explanation"
}}

For document-only retrieval:

{{
    "retrieve_memory": false,
    "retrieve_documents": true,
    "blocks": [],
    "reason": "short explanation"
}}

For both:

{{
    "retrieve_memory": true,
    "retrieve_documents": true,
    "blocks": ["project"],
    "reason": "short explanation"
}}

For no retrieval:

{{
    "retrieve_memory": false,
    "retrieve_documents": false,
    "blocks": [],
    "reason": "short explanation"
}}

IMPORTANT:

The "blocks" field may ONLY contain:

"user"
"project"
"hobby"
"academics"
"work"
"other"

Do not add any other values.

Do not write anything outside the JSON.
"""

        result = self.generate_json(
            prompt
        )

        # =================================
        # SAFETY DEFAULTS
        # =================================

        result.setdefault(
            "retrieve_memory",
            False
        )

        result.setdefault(
            "retrieve_documents",
            False
        )

        result.setdefault(
            "blocks",
            []
        )

        result.setdefault(
            "reason",
            ""
        )

        # =================================
        # VALIDATE BLOCKS
        # =================================

        allowed = {
            "user",
            "project",
            "hobby",
            "academics",
            "work",
            "other"
        }

        if not isinstance(
            result["blocks"],
            list
        ):

            result["blocks"] = []

        result["blocks"] = [
            block
            for block in result["blocks"]
            if block in allowed
        ]

        # =================================
        # FORCE BOOLEAN VALUES
        # =================================

        result["retrieve_memory"] = bool(
            result["retrieve_memory"]
        )

        result["retrieve_documents"] = bool(
            result["retrieve_documents"]
        )

        return result