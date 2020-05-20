#!/bin/env python3
from aiohttp import web
import asyncio
import discord
import json
import threading
import time

class DiscordClient(discord.Client):
    async def on_ready(self):
        print('[INFO] Discord: Logged on as {0}!'.format(self.user))

async def fetch_by_id(request):
    uid = request.match_info['uid']
    print("[INFO] fetch_by_id: Searching for uid: ", uid)
    discord_user = await client.fetch_user(uid)
    user = {
            "uid": discord_user.id,
            "tag": discord_user.name + "#" + discord_user.discriminator,
            "avatar": discord_user.avatar,
            "bot": discord_user.bot,
            "created_at": int(time.mktime(discord_user.created_at.timetuple()))
    }
    return web.Response(text=json.dumps(user))


async def run_bot(token):
    await client.start(token)

def run_it_forever(loop):
    loop.run_forever()

def init(token):
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot(token))

    thread = threading.Thread(target=run_it_forever, args=(loop, ))
    app = web.Application()
    app.add_routes([web.get('/{uid}', fetch_by_id)])
    web.run_app(app)
    thread.join()

token = os.environ['DISCORD_TOKEN']
client = DiscordClient()
init(token)
