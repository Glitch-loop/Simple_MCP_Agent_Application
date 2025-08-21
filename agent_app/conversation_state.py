from agents import TResponseInputItem
from interfaces.interfaces import text_message

class ConversationState:
    def __init__(self):
        self.history:list[text_message|list[TResponseInputItem]] = []

    def add_message(self, role: str, content: str):
            users_message:text_message = text_message(
                role=role,
                content=content
            )
            self.history.append(users_message.dict())

    def update_history(self, chat:list[TResponseInputItem]):
        """
            Function that updates the chat history.
        """

        self.history.clear()
        self.history.extend(chat)

    def get_history(self):
        return self.history
    
    def clear_history(self):
        self.history.clear()
        return "Conversation history cleared."
    