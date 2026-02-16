from openai import OpenAI
from config import Settings

class OpenAIChat:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = OpenAI(api_key=settings.openai_api_key)

    def ask(self, user_text: str) -> str:
        """
        Synchronous call (simple + reliable). For higher throughput, we can convert to async later.
        """
        user_text = (user_text or "").strip()
        if not user_text:
            return "Please provide a question after `$question`."

        resp = self.client.chat.completions.create(
            model=self.settings.openai_model,
            messages=[
                {"role": "system", "content": self.settings.system_prompt},
                {"role": "user", "content": user_text},
            ],
            temperature=0.6,
        )

        return (resp.choices[0].message.content or "").strip() or "I couldn't generate a response."
