from typing import List

DISCORD_LIMIT = 2000

def chunk_text(text: str, limit: int = DISCORD_LIMIT) -> List[str]:
    text = text or ""
    if len(text) <= limit:
        return [text]

    chunks: List[str] = []
    start = 0
    while start < len(text):
        end = min(start + limit, len(text))
        # try to break at a newline for nicer formatting
        nl = text.rfind("\n", start, end)
        if nl != -1 and nl > start + 200:
            end = nl
        chunks.append(text[start:end])
        start = end
    return chunks
