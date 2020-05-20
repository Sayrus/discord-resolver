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
- `/health` will return yes if Discord is ready and websocket is open

## Why?
I was bored and ReCaptcha on `discord.id` were taking too much time. I didn't
find a self-hosted version of it so I made one.

# TODO

A lot of things:
- UI (Feel free to do a PR)
- Check if the UID is a valid Snowflake
- Handle errors
