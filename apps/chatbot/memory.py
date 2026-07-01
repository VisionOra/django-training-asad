from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from .prompts import SYSTEM_PROMPT


def build_message_history(session):
    """
    Convert this session's DB messages into LangChain message objects,
    starting with the system prompt.
    """
    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    for msg in session.messages.all().order_by("created_at"):
        if msg.role == "user":
            messages.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            messages.append(AIMessage(content=msg.content))

    return messages
