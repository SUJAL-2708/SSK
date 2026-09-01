from models.granite import Granite


class MemoryClassifier:

    def __init__(self):

        self.granite = Granite()

    def classify(
        self,
        content: str
    ) -> str:

        result = self.granite.classify_memory(
            content
        )

        return result["block"]