# Discord Resolver

Discord resolver is an open-source version that retrieve the following
information from a Discord UID:
- Full Tag (Name#Discriminator)
- Avatar
- Bot Status
- Account creation date

## Run it

Get a Discord bot token
`docker run -p 8080:8080 -e DISCORD_TOKEN=<your_token> esayrus/discord-resolver`

Navigate to `localhost:8080/by-uid/<uid>` and you will get the information as a JSON.

### Healthcheck

- `/alive` will always return `yes`
- `/health` will return `yes` if Discord is ready and websocket is open.
  Otherwise it will return `no`.

## Why?

I was bored and ReCaptcha on `discord.id` was taking too much time. I didn't
find a self-hosted version of it so I made one.

As a Discord administrator, this kind of tool is very useful (at least in my use
case). It used to be possible to just type the UID in the address bar but
Discord removed it unless you have a common guild.

## How does it work

Unlike the "user" API, the Bot API is still allowed to retrieve any user from
his UID. This project uses this API to fetch it.

# TODO

A lot of things:
- UI (Feel free to do a PR)
- Check if the UID is a valid Snowflake
- Handle errors
