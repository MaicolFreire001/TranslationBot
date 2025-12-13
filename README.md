#🤖 TranslatorBot - Discord Translation Bot
TranslatorBot is a modular Discord bot built with discord.py that offers automatic message translation, on-demand translation via emoji reactions, and a right-click context menu to select the target language. Server configurations are persistently saved using SQLite.

###✨ Key Features
Contextual Translation: Use the Right-Click menu on any message to open a dropdown and select the target language instantly.

Reaction Translation: Quickly translate messages by reacting with a country flag emoji (e.g., 🇪🇸 for Spanish).

Per-Server Auto-Translation: Use the /toggle_auto command to enable/disable automatic translation and /set-language to set the default target language for the server.

Data Persistence: Uses SQLite to save configurations for each guild, ensuring data remains persistent across restarts or deployments.

Modular Architecture: Organized into Cogs for easy scalability and maintenance.

###🛠️ Requirements and Setup

1. System Requirements
Python 3.10 or higher (tested with Python 3.12).

A Discord Account and a configured Bot Application.

2. Clone the Repository
Bash

git clone [https://github.com/MaicolFreire001/TranslationBot.git]
cd translator-bot

3. Virtual Environment and Dependencies
Using a virtual environment (venv) is highly recommended:

Bash
Create virtual environment
python -m venv .venv

Activate virtual environment
  On Windows:
    .\.venv\Scripts\activate
  On macOS/Linux:
    source .venv/bin/activate

### Install dependencies
pip install -r requirements.txt

##⚙️ Environment Configuration (.env)
You need an environment file (.env) in the project's root folder to store your sensitive tokens and IDs.

Create a file named .env in your main project folder (translator-bot/).

Get the Token from your Discord Developer Portal application.

Enter your credentials in the .env file:

-SECRET BOT TOKEN
DISCORD_TOKEN="YOUR_TOKEN_FROM_DISCORD_DEVELOPER_PORTAL"

-Application ID (Client ID)
APP_ID="YOUR_APPLICATION_ID"

-Optional: ID of a server for quick slash command synchronization (development/testing)
GUILD_ID="ID_OF_A_TEST_SERVER"

##▶️ Running Locally
With the environment activated and .env configured, you can start the bot:

Bash
python bot.py

The bot will connect to Discord, sync the slash commands (/), and will be ready for use.

##📂 Project Structure
The bot uses a modular architecture based on Cogs, making it easy to add new functionalities.

translator-bot/
├─ bot.py               - Main entry point
├─ .env                 - Environment variables
├─ requirements.txt     - Dependencies
├─ bot_config.db        - SQLite database file (persistent)
├─ utils/
│  ├─ db_manager.py     - DB Logic: get_config, update_config (SQLite)
│  └─ translator.py     - Translation utilities (Deep Translator, language detection)
└─ cogs/
   ├─ admin.py          - /set-language and /toggle_auto commands
   ├─ context_translate.py - Right-click context menu
   ├─ reactions.py      - Emoji reaction translation logic
   └─ auto_server.py    - on_message listener for automatic translation
   
##☁️ Production Deployment (24/7)
This bot is structured to be deployed on hosting services that support containers, such as Railway.

####Railway Configuration
To maintain the persistence of the configuration data (bot_config.db) across restarts and deployments, you must configure an External Volume in Railway.

####Git Connection: Connect Railway to your repository.

####Variables: Add the DISCORD_TOKEN and APP_ID variables to Railway's Environment Variables.

####Persistence: Create a Volume service in Railway (e.g., bot-data).

####Volume Mount: Mount the created volume to the path /app/data. Your utils/db_manager.py file must be configured to point to this location (/app/data/bot_config.db).

####The Procfile in the root directs the execution:
web: python bot.py

###Developed by: [Maicol Freire / https://github.com/MaicolFreire001]
