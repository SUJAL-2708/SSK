from dataclasses import dataclass
from typing import Optional


@dataclass
class Memory:

    memory_id: str

    content: str

    block: str

    importance: int


@dataclass
class MemoryDecision:

    retrieve: bool

    blocks: list

    reason: str


@dataclass
class RetrievedMemory:

    memory_id: str

    content: str

    block: str

    importance: int

    distance: Optional[float] = None