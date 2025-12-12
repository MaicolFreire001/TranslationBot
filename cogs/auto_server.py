import discord
from discord.ext import commands
from utils.translator import translate_text, build_translation_embed
from utils.db_manager import get_config

class AutoTranslate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if message.author.bot:
            return

        guild_id = message.guild.id

        if not guild_id: return 
        
        config = get_config(guild_id)
        
        if not config['auto']: return 
        
        translated, detected_lang = await translate_text(
            message.content,
            config['lang']
        )

        if translated.lower() == message.content.lower():
            return

        embed = build_translation_embed(
            original_text=message.content,
            translated_text=translated,
            detected_lang=detected_lang,
            target_lang=config['lang'],
            author=message.author,
            guild_icon_url=message.guild.icon.url if message.guild and message.guild.icon else None
        )

        try:
            await message.reply(embed=embed, mention_author=False)
        except:
            pass


async def setup(bot):
    await bot.add_cog(AutoTranslate(bot))
