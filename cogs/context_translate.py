import discord
from discord.ext import commands
from discord import app_commands
from utils.translator import translate_text, build_translation_embed

LANG_OPTIONS = {
    "es": "Spanish",
    "en": "English",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ja": "Japanese",
    "ko": "Korean",
    "zh": "Chinese",
    "ru": "Russian",
}

@app_commands.context_menu(name="Translate Message")
async def translate_context_menu(interaction: discord.Interaction, message: discord.Message):

    if not message.content or not message.content.strip():
        return await interaction.response.send_message(
            "This message has no text to translate.",
            ephemeral=True
        )

    class LangDropdown(discord.ui.Select):
        def __init__(self):
            options = [
                discord.SelectOption(label=name, value=code)
                for code, name in LANG_OPTIONS.items()
            ]
            super().__init__(
                placeholder="Choose language…",
                min_values=1,
                max_values=1,
                options=options
            )

        async def callback(self, drop_inter: discord.Interaction):
            lang = self.values[0]

            translated, detected_lang = await translate_text(
                message.content,
                lang
            )

            embed = build_translation_embed(
                original_text=message.content,
                translated_text=translated,
                detected_lang=detected_lang,
                target_lang=lang,
                author=message.author,
                guild_icon_url=message.guild.icon.url if message.guild and message.guild.icon else None
            )

            await drop_inter.response.edit_message(
                content=None,
                embed=embed,
                view=None
            )

    class DropdownView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=60)
            self.add_item(LangDropdown())

    await interaction.response.send_message(
        f"Translate message:\n```{message.content}```",
        view=DropdownView(),
        ephemeral=True
    )

class ContextTranslate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.bot.tree.add_command(translate_context_menu)

    async def cog_unload(self):
        self.bot.tree.remove_command("Translate Message", type=app_commands.ContextMenu)


async def setup(bot):
    await bot.add_cog(ContextTranslate(bot))
