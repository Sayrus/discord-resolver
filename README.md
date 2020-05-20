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

Navigate to `localhost:8080/<uid>` and you will get the information as a JSON.

## Why?
I was bored and ReCaptcha on `discord.id` were taking too much time. I didn't
find a self-hosted version of it so I made one.
