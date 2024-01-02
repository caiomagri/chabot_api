from abc import ABC, abstractmethod


class AIApiClient(ABC):
    @abstractmethod
    def execute_chat_completion(self, prompt: str):
        """
        Send prompt to AI api using chat completion
        Args:
            prompt (list[dict[str, Any]]): Prompt
        """
        raise NotImplementedError
