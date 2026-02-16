import discord
from discord.ext import commands

from config import get_settings
from openai_client import OpenAIChat
from utils import chunk_text

settings = get_settings()
ai = OpenAIChat(settings)

intents = discord.Intents.default()
intents.message_content = True  # REQUIRED for prefix commands to read text
bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (id={bot.user.id})")

@bot.command(name="hello")
async def hello(ctx: commands.Context):
    await ctx.send("Hello! 👋")

@bot.command(name="question", aliases=["q"])
async def question(ctx: commands.Context, *, prompt: str = ""):
    # Show "typing..." while we call the model
    async with ctx.typing():
        try:
            answer = ai.ask(prompt)
        except Exception as e:
            await ctx.send(f"Error calling OpenAI: `{type(e).__name__}: {e}`")
            return

    # Send in chunks (Discord message limit)
    for part in chunk_text(answer):
        await ctx.send(part)

if __name__ == "__main__":
    bot.run(settings.discord_token)
