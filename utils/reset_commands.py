import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
APP_ID = os.getenv("APP_ID")
GUILD_ID = os.getenv("GUILD_ID")  # Opcional

HEADERS = {
    "Authorization": f"Bot {TOKEN}",
    "Content-Type": "application/json"
}

def reset_global_commands():
    url = f"https://discord.com/api/v10/applications/{APP_ID}/commands"
    print("🔄 Eliminando comandos GLOBALS…")

    r = requests.put(url, headers=HEADERS, json=[])
    if r.status_code in (200, 201, 204):
        print("✅ Comandos globales eliminados.")
    else:
        print("❌ Error:", r.status_code, r.text)

def reset_guild_commands():
    if not GUILD_ID:
        print("⚠ No GUILD_ID definido en .env, solo se limpiarán comandos globales.")
        return

    url = f"https://discord.com/api/v10/applications/{APP_ID}/guilds/{GUILD_ID}/commands"
    print(f"🔄 Eliminando comandos del servidor {GUILD_ID}…")

    r = requests.put(url, headers=HEADERS, json=[])
    if r.status_code in (200, 201, 204):
        print("✅ Comandos del servidor eliminados.")
    else:
        print("❌ Error:", r.status_code, r.text)


if __name__ == "__main__":
    reset_global_commands()
    reset_guild_commands()
    print("✨ Listo. Ahora reinicia tu bot.")
