class ConversationManager:
    """
    Simple in-memory conversation manager.
    Stores chat history per session.
    """

    def __init__(self):
        self.history = []

    def add_user_message(self, content: str):
        self.history.append({"role": "user", "content": content})

    def add_ai_message(self, content: str):
        self.history.append({"role": "assistant", "content": content})

    def get_history(self):
        return self.history

    def clear(self):
        self.history = []
# app/memory/conversation.py
