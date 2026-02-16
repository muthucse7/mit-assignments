# Assignment 3 — Conceiving of and Designing Agents

This folder contains the code and supporting files for Option 1: a simple Discord agent (bot) built as part of Assignment 3. The project demonstrates a minimal agent loop (listen → reason → act) and includes optional integration points for an LLM via the OpenAI SDK.

Repository contents (key files)
- `bot.py` — main Discord bot implementation (event handlers/commands).
- `config.py` — configuration helpers and constants.
- `openai_client.py` — optional OpenAI wrapper used to call an LLM (if enabled).
- `utils.py` — small utility functions used by the bot.
- `requirements.txt` — pinned Python dependencies for the project.
- `.venv/` — (local) virtual environment (not tracked); create your own as described below.

Project overview
- The bot connects to Discord using a bot token, listens for commands (for example `!ping`, `!echo`), and responds in-channel. The code is intentionally small so you can extend it to demonstrate agent behaviors such as simple state, scheduled tasks, or LLM-driven intent parsing.

Prerequisites
- Python 3.10+
- Discord account and a test server you control
- (Optional) An OpenAI API key if you plan to enable LLM features in `openai_client.py`

Setup (macOS, zsh)
1. Create and activate a virtual environment:
   python3 -m venv .venv
   source .venv/bin/activate

2. Install dependencies:
   pip install -U pip
   pip install -r requirements.txt

3. Add environment variables (create a `.env` file at the project root):
   DISCORD_TOKEN=your_discord_bot_token_here
   # Optional for LLM features
   OPENAI_API_KEY=your_openai_api_key_here

   Note: Do NOT commit `.env` to version control.

Create and invite Discord bot
- Use https://discord.com/developers/applications to create an application, add a Bot, copy the token, and invite the bot to a server with the `bot` scope and permissions to read/send messages.

Run the bot
With the venv activated and `.env` present:
   python bot.py

Expected behavior
- On startup the bot logs a ready message with its username.
- `!ping` should elicit `Pong`.
- `!echo hello` should reply `hello`.
- If OpenAI is enabled, some commands can route input to the LLM for richer responses (see `openai_client.py`).

Testing and debugging
- Watch the terminal for tracebacks and helpful logs.
- Verify permissions and token validity if the bot doesn't connect.
- Use a dedicated test server to avoid accidental spam.

Deliverables for the assignment
- `bot.py` and any supporting modules you modified.
- A 1–2 paragraph write-up describing design choices and how the agent reasons and acts.
- Two images placed in this folder (or linked from the repo root):
  1) `mockup.png` — a mockup of your original idea.
  2) a screenshot of the Assignment 2 HTML page (e.g., copy `../Assignment_2_Vibe_Coding/Generated_UI_Code_html.png`).
- Optional: short demo video or screenshots showing bot responding in Discord.

Extensions and ideas
- Add a simple task queue or scheduler (reminders, background checks).
- Persist small state with SQLite for user preferences or reminders.
- Integrate conversational intent parsing via the OpenAI client and route commands to LLM responses.

References
- discord.py docs: https://discordpy.readthedocs.io/
- OpenAI Python SDK docs: https://pypi.org/project/openai/

If you want, I can add a minimal example `bot.py` command set, or wire a small demo that uses the OpenAI client for one command. Reply with which option you prefer.
