import discord
from discord.ext import commands
from discord import app_commands
from utils.db_manager import update_config, get_config
from typing import Dict

LANGUAGES: Dict[str, str] = {
    "Spanish": "es",
    "English": "en",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese (Simplified)": "zh-CN",
    "Russian": "ru"
}


class LanguageSelect(discord.ui.Select):
    def __init__(self, guild_id):
        self.guild_id = guild_id

        options = [
            discord.SelectOption(label=name, value=code)
            for name, code in LANGUAGES.items()
        ]

        super().__init__(
            placeholder="Select the server language...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        update_config(interaction.guild_id, lang=self.values[0])
        
        selected_name = next((name for name, code in LANGUAGES.items() if code == self.values[0]), self.values[0])

        await interaction.response.edit_message(
            content=f"🌐 Server translation target language set to **{selected_name}** (`{self.values[0]}`).",
            view=None
        )

class LanguageView(discord.ui.View):
    def __init__(self, guild_id):
        super().__init__(timeout=60)
        self.add_item(LanguageSelect(guild_id))


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(
        name="set-language",
        description="Choose the server's main translation target language."
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def set_language(self, interaction: discord.Interaction):
        if not interaction.guild:
            await interaction.response.send_message("This command must be used in a server.", ephemeral=True)
            return

        view = LanguageView(interaction.guild_id)
        await interaction.response.send_message(
            "Choose the main translation language for this server:",
            view=view,
            ephemeral=True
        )

    @app_commands.command(
        name="toggle_auto",
        description="Enable or disable automatic translation in the server."
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def toggle_auto(self, interaction: discord.Interaction):
        if not interaction.guild:
            await interaction.response.send_message("This command must be used in a server.", ephemeral=True)
            return
            
        cfg = get_config(interaction.guild_id)
        current = cfg.get("auto", False)
        
        new_state = not current
        update_config(interaction.guild_id, auto=new_state)

        state = "enabled" if new_state else "disabled"
        
        current_lang = cfg.get("lang", "es") 
        
        await interaction.response.send_message(
            f"🔄 Auto-translation is now **{state}**.\n"
            f"The current target language is `{current_lang}`.",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Admin(bot))