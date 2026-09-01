import json
import redis

from config.settings import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB,
    REDIS_KEY,
    MESSAGE_LIMIT
)


class RedisMemory:

    def __init__(self):

        self.client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True
        )

        self.key = REDIS_KEY

    # =====================================
    # ADD MESSAGE
    # =====================================

    def add_message(
        self,
        role: str,
        content: str
    ):

        message = {
            "role": role,
            "content": content
        }

        self.client.rpush(
            self.key,
            json.dumps(message)
        )

    # =====================================
    # GET MESSAGES
    # =====================================

    def get_messages(self) -> list:

        raw_messages = self.client.lrange(
            self.key,
            0,
            -1
        )

        return [
            json.loads(message)
            for message in raw_messages
        ]

    # =====================================
    # COUNT
    # =====================================

    def count(self) -> int:

        return self.client.llen(
            self.key
        )

    # =====================================
    # LIMIT CHECK
    # =====================================

    def limit_reached(self) -> bool:

        return self.count() >= MESSAGE_LIMIT

    # =====================================
    # CLEAR AFTER CONSOLIDATION
    # =====================================

    def clear(self):

        self.client.delete(
            self.key
        )

    # =====================================
    # FORMAT FOR LLM
    # =====================================

    def formatted(self) -> str:

        messages = self.get_messages()

        return "\n".join(
            f"{message['role'].upper()}: "
            f"{message['content']}"
            for message in messages
        )