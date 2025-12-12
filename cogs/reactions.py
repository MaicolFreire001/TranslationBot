import discord
from discord.ext import commands
from utils.translator import translate_text, build_translation_embed

REACTION_LANG = {
    "🇪🇸": "es",
    "🇺🇸": "en",
    "🇫🇷": "fr",
    "🇩🇪": "de",
    "🇮🇹": "it",
    "🇵🇹": "pt",
    "🇯🇵": "ja",
    "🇰🇷": "ko",
    "🇨🇳": "zh",
    "🇷🇺": "ru",
}

class ReactionTranslate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):

        if user.bot:
            return

        emoji = str(reaction.emoji)
        if emoji not in REACTION_LANG:
            return

        msg = reaction.message
        target_lang = REACTION_LANG[emoji]

        translated, detected_lang = await translate_text(
            msg.content,
            target_lang
        )

        if translated.lower() == msg.content.lower():
            return

        embed = build_translation_embed(
            original_text=msg.content,
            translated_text=translated,
            detected_lang=detected_lang,
            target_lang=target_lang,
            author=msg.author,
            guild_icon_url=msg.guild.icon.url if msg.guild and msg.guild.icon else None
        )

        try:
            await msg.reply(embed=embed, mention_author=False)
        except:
            pass


async def setup(bot):
    await bot.add_cog(ReactionTranslate(bot))
