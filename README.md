# Discord Resolver

Discord resolver is an open-source version that retrieves the following information from a Discord UID:
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

# Features

- **User Interface**: A simple Tkinter-based UI is now available to input a Discord UID and check if it is a valid Snowflake.
- **Snowflake Validation**: The script now includes a function to validate if a given UID is a valid Snowflake ID, ensuring it is a 64-bit integer within the valid range for a Snowflake ID, considering the Discord epoch ^1^.
- **Error Handling**: The script has been enhanced with error handling to catch and manage exceptions, providing informative error messages to the user.

# Usage

1. **Run the Docker Container**:
   ```sh
   docker run -p 8080:8080 -e DISCORD_TOKEN=<your_token> esayrus/discord-resolver
   ```

2. **Access the API**:
   - Navigate to `localhost:8080/by-uid/<uid>` to retrieve user information.
   - Use `/alive` to check if the service is running.
   - Use `/health` to check the health status of the Discord connection.

3. **Use the UI**:
   - Run the script, and a Tkinter window will appear.
   - Enter a Discord UID and click "Check UID" to validate if it is a Snowflake ID.

# Error Handling

The script now includes robust error handling to manage exceptions and provide meaningful error messages. This ensures that any issues during the execution of the script are caught and reported back to the user.

# Snowflake Validation

The script validates if a given UID is a valid Snowflake ID. A Snowflake ID is a 64-bit integer composed of a timestamp, node ID, and sequence number. The validation ensures the UID is within the valid range and format for a Snowflake ID, considering the Discord epoch ^1^.

# Contributing

Feel free to contribute by adding new features, improving the UI, or enhancing error handling. Pull requests are welcome!

# License

This project is licensed under the MIT License.