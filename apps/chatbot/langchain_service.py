from decouple import config
from langchain_groq import ChatGroq
from .memory import build_message_history
from langchain_core.messages import HumanMessage


def get_ai_response(session, user_content: str) -> str:
    """
    Build conversation history + new user message, call Groq,
    return AI reply text. Raises RuntimeError with a user-friendly
    message if the API key is missing or the call fails.
    """
    api_key = config("GROQ_API_KEY", default="")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to your .env file."
        )

    try:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            groq_api_key=api_key,
            temperature=0.7,
            max_tokens=1024,
        )

        messages = build_message_history(session)
        messages.append(HumanMessage(content=user_content))

        response = llm.invoke(messages)
        return response.content

    except Exception as exc:
        raise RuntimeError(f"AI service error: {exc}") from exc
