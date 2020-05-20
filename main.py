#!/bin/env python3
from aiohttp import web
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
        print('[INFO] Discord: Logged on as {0}!'.format(self.user))

    def is_ready(self):
        return self.ready

async def fetch_by_id(request):
    uid = request.match_info['uid']
    if not uid.isnumeric():
        return web.Response(text=json.dumps({error:"UID must be numeric"}))
    print("[INFO] fetch_by_id: Searching for uid:", uid)
    discord_user = await client.fetch_user(uid)
    user = {
            "uid": discord_user.id,
            "tag": discord_user.name + "#" + discord_user.discriminator,
            "avatar": discord_user.avatar,
            "bot": discord_user.bot,
            "created_at": int(time.mktime(discord_user.created_at.timetuple()))
    }
    return web.Response(text=json.dumps(user))

async def handle_health(request):
    if not client.is_ready() or client.is_closed():
        return web.Response(text="no")
    return web.Response(text="yes")

async def alive(request):
    return web.Response(text="yes")

async def run_bot(token):
    await client.start(token)

def run_it_forever(loop):
    loop.run_forever()

token = os.environ['DISCORD_TOKEN']

client = DiscordClient()
loop = asyncio.get_event_loop()
loop.create_task(run_bot(token))

thread = threading.Thread(target=run_it_forever, args=(loop, ))

app = web.Application()
app.add_routes([web.get('/health', handle_health),
                web.get('/alive', alive),
                web.get('/by-uid/{uid}', fetch_by_id)])
web.run_app(app)

# This should be useless as web.run_app is a blocking call and the loop run ... forever
thread.join()
