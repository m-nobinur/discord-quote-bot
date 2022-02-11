"""
Name: discord-quote-bot
Description: This is a template to create your own discord bot in python.
Author: Mohammad Nobinur

Using https://github.com/DisnakeDev/disnake
API: http://disnake.readthedocs.io/en/latest/api.html

Copyright © m-nobinur 2022 - https://github.com/m-nobinur

"""

import disnake
from disnake.ext import commands
import requests

import sys
import re
import random


BOT_USER_TOKEN = None
BASE_URL = "https://api.quotable.io"


def get_random_quote(url=BASE_URL, tags=None, length=None):
    url = f"{BASE_URL}/random"

    if tags is not None and length is None:
        url = f"{url}?tags={tags}"
    elif length is not None and tags is None:
        if "-" in length:
            try:
                a, b = length.split("-")
                url = f"{url}?minLength={a}&maxLength={b}"
            except Exception as e:
                print("Error on spliting maxlength.")
        else:
            url = f"{url}?maxLength={length}"
    elif length is not None and tags is not None:
        if "-" in length:
            try:
                a, b = length.split("-")
                url = f"{url}?tags={tags}&?minLength={a}&maxLength={b}"
            except Exception as e:
                print("Error on spliting maxlength.")
        else:
            url = f"{url}?tags={tags}&?maxLength={length}"

    try:
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            quote, author = data.get("content"), data.get("author")
            return (quote, author)
        else:
            print("Can't find a quote!")

    except Exception as e:
        print(e)


class QuoteBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or(">"))

    async def on_ready(self):
        print(f"Logged in as {self.user.name}")


bot = QuoteBot()
color = ["css", "bash", "ini", "fix", " "]
quote_template = """```{}
["{}"]
``` - *{}*
"""


@bot.command()
async def quote(ctx: commands.Context, *, args: str = None):
    tags, length = None, None
    if args:
        match_tags = re.search("tags=(\w+,*\w*)\s?", args)
        match_length = re.search("len=(\d+-?\d*)\s?", args)
        tags = match_tags.group(1) if match_tags is not None else None
        length = match_length.group(1) if match_length is not None else None

    msg = await ctx.send("Getting quote........")

    if tags and length:
        quote_data = get_random_quote(tags=tags, length=length)
    elif tags is not None and length is None:
        quote_data = get_random_quote(tags=tags)
    elif tags is None and length is not None:
        quote_data = get_random_quote(length=length)
    else:
        quote_data = get_random_quote()

    if quote_data:
        quote, author = quote_data
        lang = random.choice(color)
        await msg.edit(content=quote_template.format(lang, quote, author))
    else:
        await msg.edit(content="Sorry! No quote found!")


if __name__ == "__main__":

    if BOT_USER_TOKEN is None:
        if len(sys.argv) < 2:
            print(
                "Set the BOT_USER_TOKEN variable in the bot.py file or pass it as an argument."
            )
            print("Usage: python bot.py BOT_USER_TOKEN")
            exit()
        else:
            BOT_USER_TOKEN = sys.argv[1]
            bot.run(BOT_USER_TOKEN)
    else:
        try:
            bot.run(BOT_USER_TOKEN)
            bot.run(sys.argv[1])
        except:
            bot.close()
