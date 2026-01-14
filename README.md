# 🤖 TranslatorBot - Discord Translation Bot

> **TranslatorBot** is a modular Discord bot built with `discord.py` that offers automatic message translation, on-demand translation via emoji reactions, and a right-click context menu to select the target language. Server configurations are persistently saved using **SQLite**.

## ✨ Key Features

* **Contextual Translation:** Use the **Right-Click** menu on any message to open a dropdown and select the target language instantly.
* **Reaction Translation:** Quickly translate messages by reacting with a country flag emoji (e.g., 🇪🇸 for Spanish).
* **Per-Server Auto-Translation:** Use the `/toggle_auto` command to enable/disable automatic translation and `/set-language` to set the default target language for the server.
* **Data Persistence:** Uses **SQLite** to save configurations for each guild, ensuring data remains persistent across restarts or deployments.
* **Modular Architecture:** Organized into **Cogs** for easy scalability and maintenance.

## 🛠️ Requirements and Setup

### 1. System Requirements

* Python 3.10 or higher (tested with Python 3.12).
* A Discord Account and a configured Bot Application.

### 2. Clone the Repository

```bash
git clone https://github.com/MaicolFreire001/TranslationBot.git
cd translator-bot
```


### 3. Virtual Environment and Dependencies
Using a virtual environment (venv) is highly recommended:

```bash
#Create virtual environment
python -m venv .venv

#Activate virtual environment
  On Windows:
    .\.venv\Scripts\activate
  On macOS/Linux:
    source .venv/bin/activate

#Install dependencies
pip install -r requirements.txt
```

## ⚙️ Environment Configuration (.env)
You need an environment file (.env) in the project's root folder to store your sensitive tokens and IDs.

Create a file named .env in your main project folder (translator-bot/).

Get the Token from your Discord Developer Portal application.

Enter your credentials in the .env file:
```bash
#SECRET BOT TOKEN
DISCORD_TOKEN="YOUR_TOKEN_FROM_DISCORD_DEVELOPER_PORTAL"

#Application ID (Client ID)
APP_ID="YOUR_APPLICATION_ID"

#Optional: ID of a server for quick slash command synchronization (development/testing)
GUILD_ID="ID_OF_A_TEST_SERVER"
```
## ▶️ Running Locally
With the environment activated and .env configured, you can start the bot:

```bash
python bot.py
```
The bot will connect to Discord, sync the slash commands (/), and will be ready for use.

## 📂 Project Structure
The bot uses a modular architecture based on Cogs, making it easy to add new functionalities.

* translator-bot/
* ├─ bot.py               - Main entry point
* ├─ .env                 - Environment variables
* ├─ requirements.txt     - Dependencies
* ├─ bot_config.db        - SQLite database file (persistent)
* ├─ utils/
* │  ├─ db_manager.py     - DB Logic: get_config, update_config (SQLite)
* │  └─ translator.py     - Translation utilities (Deep Translator, language detection)
* └─ cogs/
*    ├─ admin.py          - /set-language and /toggle_auto commands
*    ├─ context_translate.py - Right-click context menu
*    ├─ reactions.py      - Emoji reaction translation logic
*    └─ auto_server.py    - on_message listener for automatic translation
   
## ☁️ Production Deployment (24/7) - Render

This bot is configured to be deployed on **Render**, which offers a permanent free tier suitable for Discord bots. Render will keep the bot running with the following key configurations:

### Render Configuration

To ensure your bot maintains **SQLite** database persistence, you must set it up as a **Cron Job** and not a standard Web Service, as Render's free Web Service does not allow file persistence.

1.  **Repo Setup:** Connect Render to your GitHub repository.
2.  **Service Type:** Create a **Cron Job** (Not a Web Service).
    * **Reason:** Render's free Web Services are ephemeral and delete the `bot_config.db` database on every redeploy or restart. Cron Jobs, by running the bot command once indefinitely, offer more stability for simple file persistence.

3.  **Cron Job Configuration:**
    * **Environment:** Python 3
    * **Build Command:** `pip install -r requirements.txt`
    * **Start Command:** `python bot.py`
    * **Schedule:** Use a Cron syntax to execute the command once but keep it active (e.g., `0 0 1 1 *` or `0 0 1 1 1`).

4.  **Environment Variables:**
    * Add the `DISCORD_TOKEN` and `APP_ID` variables (and `GUILD_ID` if used for development).

### ⚠️ Important Note on Persistence

* Render does not offer true persistent storage (Volumes) on the Free Tier.
* **Ensure your `utils/db_manager.py` attempts to create the database (`bot_config.db`) in the application directory if it doesn't exist.** When using a Cron Job, this database file *usually* persists through service idle cycles, provided there isn't a *re-deploy* or forced rebuild. For critical long-term data persistence, you should consider a free external database (like MongoDB Atlas Free Tier).

  
#### Developed by: [Maicol Freire / https://github.com/MaicolFreire001]
