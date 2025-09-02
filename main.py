#!/bin/env python3
from aiohttp import web
import asyncio
import discord
import json
import os
import threading
import time
import re
import tkinter as tk
from tkinter import messagebox

# Function to check if the UID is a valid Snowflake
def is_valid_snowflake(uid):
    # Snowflake IDs are 64-bit integers, which means they can have up to 18 digits
    # They are also time-sortable, so they must be greater than the Discord epoch
    discord_epoch = int(time.mktime(time.strptime('2015-01-01', '%Y-%m-%d')))
    return re.match(r'^\d{17,19}$', uid) and int(uid) > discord_epoch

# Error handling decorator
def handle_errors(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            await args[0].send(f"An error occurred: {e}")
    return wrapper

class DiscordClient(discord.Client):
    ready = False
    async def on_ready(self):
        self.ready = True
        print('[INFO] Discord: Logged on as {0}!'.format(self.user))

    def is_ready(self):
        return self.ready

async def fetch_by_id(request):
    uid = request.match_info['uid']
    if not is_valid_snowflake(uid):
        return web.Response(text=json.dumps({"error": "UID must be a valid Snowflake ID"}))
    print("[INFO] fetch_by_id: Searching for uid:", uid)
    try:
        discord_user = await client.fetch_user(uid)
        user = {
            "uid": discord_user.id,
            "tag": discord_user.name + "#" + discord_user.discriminator,
            "avatar": str(discord_user.avatar),
            "bot": discord_user.bot,
            "created_at": int(time.mktime(discord_user.created_at.timetuple()))
        }
        return web.Response(text=json.dumps(user))
    except discord.errors.NotFound:
        return web.Response(text=json.dumps({"error": "User not found"}))
    except discord.errors.HTTPException as e:
        return web.Response(text=json.dumps({"error": str(e)}))
    except Exception as e:
        return web.Response(text=json.dumps({"error": "An unexpected error occurred"}))

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

# UI for the bot
class BotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Discord Bot UI")

        self.label = tk.Label(root, text="Enter Discord UID:")
        self.label.pack()

        self.entry = tk.Entry(root)
        self.entry.pack()

        self.check_button = tk.Button(root, text="Check UID", command=self.check_uid)
        self.check_button.pack()

        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

    def check_uid(self):
        uid = self.entry.get()
        if is_valid_snowflake(uid):
            messagebox.showinfo("Result", f"The UID {uid} is a valid Snowflake.")
        else:
            messagebox.showinfo("Result", f"The UID {uid} is not a valid Snowflake.")

# Create the UI
root = tk.Tk()
ui = BotUI(root)
root.mainloop()