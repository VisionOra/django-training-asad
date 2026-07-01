import requests
from decouple import config


SERPER_URL = "https://google.serper.dev/search"


def fetch_sources(topic: str, limit: int = 10) -> list[dict]:
    """
    Query the Serper API for organic search results on a given topic.
    Returns a list of dicts with keys: title, link, snippet, position.
    Raises RuntimeError if the API key is missing or the request fails.
    """
    api_key = config("SERPER_API_KEY", default="")
    if not api_key:
        raise RuntimeError("SERPER_API_KEY is not set. Add it to your .env file.")

    try:
        response = requests.post(
            SERPER_URL,
            headers={
                "X-API-KEY": api_key,
                "Content-Type": "application/json",
            },
            json={"q": topic, "num": limit},
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"Serper API request failed: {exc}") from exc

    organic = response.json().get("organic", [])

    return [
        {
            "title":    result.get("title", ""),
            "link":     result.get("link", ""),
            "snippet":  result.get("snippet", ""),
            "position": result.get("position", index + 1),
        }
        for index, result in enumerate(organic[:limit])
    ]
