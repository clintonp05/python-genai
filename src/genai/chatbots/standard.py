from .base import Chatbot, ChatRequest, ChatResponse

class StandardBot(Chatbot):
    def chat(self, request: ChatRequest) -> ChatResponse:
        return ChatResponse(
            message=f"Standard response to: {request.message}",
            metadata={"type": "standard"}
        )