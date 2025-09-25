#!/bin/env python3
from aiohttp import web
from aiohttp.web import FileResponse
import asyncio
import discord
import json
import os
import threading
import time


class DiscordClient(discord.Client):
    ready = False

    async def on_ready(self):
        self.ready = True
        print("[INFO] Discord: Logged on as {0}!".format(self.user))

    def is_ready(self):
        return self.ready


async def fetch_by_id(request):
    uid = request.match_info["uid"]
    if not uid.isnumeric():
        return web.Response(text=json.dumps({"error": "UID must be numeric"}))

    if not client.is_ready() or client.is_closed():
        return web.Response(text=json.dumps({"error": "Discord client not ready"}))

    print("[INFO] fetch_by_id: Searching for uid:", uid)
    try:
        discord_user = await client.fetch_user(uid)
        user = {
            "uid": discord_user.id,
            "tag": discord_user.name + "#" + discord_user.discriminator,
            "avatar": str(discord_user.avatar) if discord_user.avatar else None,
            "bot": discord_user.bot,
            "created_at": int(time.mktime(discord_user.created_at.timetuple())),
        }
        return web.Response(text=json.dumps(user))
    except discord.NotFound:
        return web.Response(text=json.dumps({"error": "User not found"}))
    except Exception as e:
        print(f"[ERROR] fetch_by_id: {e}")
        return web.Response(text=json.dumps({"error": "Internal server error"}))


async def handle_health(request):
    if not client.is_ready() or client.is_closed():
        return web.Response(text="no")
    return web.Response(text="yes")


async def alive(request):
    return web.Response(text="yes")


async def serve_home(request):
    return FileResponse('static/home.html')


async def run_bot(token):
    await client.start(token)




token = os.environ["DISCORD_TOKEN"]

intents = discord.Intents.default()
client = DiscordClient(intents=intents)

async def init_app():
    # Start the Discord bot in the background
    asyncio.create_task(run_bot(token))

    # Create and configure the web app
    app = web.Application()
    app.add_routes(
        [
            web.get("/", serve_home),
            web.get("/health", handle_health),
            web.get("/alive", alive),
            web.get("/by-uid/{uid}", fetch_by_id),
        ]
    )
    return app

# Run the application
web.run_app(init_app())
