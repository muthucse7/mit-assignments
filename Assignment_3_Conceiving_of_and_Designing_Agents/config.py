import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    discord_token: str
    openai_api_key: str
    openai_model: str
    system_prompt: str

def get_settings() -> Settings:
    discord_token = os.getenv("TOKEN", "").strip()
    openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()
    openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
    system_prompt = os.getenv(
        "SYSTEM_PROMPT",
        "You are a helpful assistant. Keep answers concise and clear."
    ).strip()

    if not discord_token:
        raise RuntimeError("Missing TOKEN in environment (.env)")
    if not openai_api_key:
        raise RuntimeError("Missing OPENAI_API_KEY in environment (.env)")

    return Settings(
        discord_token=discord_token,
        openai_api_key=openai_api_key,
        openai_model=openai_model,
        system_prompt=system_prompt,
    )
