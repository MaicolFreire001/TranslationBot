from deep_translator import GoogleTranslator
from langdetect import detect
import asyncio
import discord

LANG_FIX = {
    "en-us": "en",
    "en-gb": "en",
    "american_english": "en",
    "british_english": "en",
    "pt-br": "pt",
    "zh": "zh-CN",
    "zh-cn": "zh-CN",
    "zh-tw": "zh-TW",
}


def flag_from_lang(code: str):

    if isinstance(code, tuple):
        code = code[0]

    if not isinstance(code, str):
        return "🏳️"

    code = code.lower()

    flags = {
        "en": "🇺🇸",
        "es": "🇪🇸",
        "fr": "🇫🇷",
        "de": "🇩🇪",
        "it": "🇮🇹",
        "pt": "🇵🇹",
        "ja": "🇯🇵",
        "ko": "🇰🇷",
        "zh-cn": "🇨🇳",
        "zh-tw": "🇹🇼",
        "ru": "🇷🇺",
    }

    return flags.get(code, "🏳️")


def safe_detect_language(text: str):
    try:
        lang = detect(text).lower()
        return LANG_FIX.get(lang, lang)
    except:
        return "unknown"



async def translate_text(text: str, target_lang: str):
    loop = asyncio.get_running_loop()
    detected = safe_detect_language(text)

    try:
        fixed_target = LANG_FIX.get(target_lang.lower(), target_lang.lower())

        translated = await loop.run_in_executor(
            None,
            lambda: GoogleTranslator(source=detected, target=fixed_target).translate(text)
        )

        return translated, detected

    except Exception as e:
        return f"Error translating: {e}", detected


def build_translation_embed(
    original_text: str,
    translated_text: str,
    detected_lang: str,
    target_lang: str,
    author: str,
    guild_icon_url: str = None
):
    embed = discord.Embed(
        color=discord.Color.blurple()
    )

    embed.title = (
        f"{flag_from_lang(detected_lang)} Detected **{detected_lang.upper()}**"
        f" → {flag_from_lang(target_lang)} **{target_lang.upper()}**"
    )

    embed.description = f"> {translated_text}"

    footer_text = (
        f"{detected_lang.lower()} → {target_lang.lower()} • "
        f"Translation for {author}"
    )

    embed.set_footer(
        text=footer_text,
        icon_url=guild_icon_url
    )

    return embed
