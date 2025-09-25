# Discord Resolver

A self-hosted Discord user lookup service that provides user information from Discord User IDs (Snowflakes).

## Features

Discord Resolver retrieves the following information from a Discord User ID:

- **Full Tag** - Username#Discriminator format
- **Avatar** - Profile picture
- **Bot Status** - Whether the account is a bot
- **Account Creation Date** - When the account was created
- **Web Interface** - UI for easy lookups
- **REST API** - JSON endpoint for programmatic access

## Quick Start

### Prerequisites
- A Discord Bot Token ([Create one here](https://discord.com/developers/applications)). The bot doesn't need to be in any servers - it just needs to exist to access Discord's API.

### Using Docker (Recommended)
```bash
docker run -p 8080:8080 -e DISCORD_TOKEN=<your_bot_token> esayrus/discord-resolver
```

### Manual Setup
```bash
git clone https://github.com/your-repo/discord-resolver
cd discord-resolver
pip install -r requirements.txt
export DISCORD_TOKEN=<your_bot_token>
python main.py
```

## Usage

### Web Interface
Open your browser and navigate to `http://localhost:8080`
- Enter a Discord User ID in the input field
- Click "Resolve User" to get user information
- View results with avatar, username, and account details

### REST API
Make GET requests to retrieve user data as JSON:
```bash
curl http://localhost:8080/by-uid/123456789012345678
```

**Example Response:**
```json
{
  "uid": 123456789012345678,
  "tag": "Username#1234",
  "avatar": "https://cdn.discordapp.com/avatars/123.../avatar.png",
  "bot": false,
  "created_at": 1420070400
}
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/by-uid/{uid}` | GET | Get user info by Discord User ID |
| `/health` | GET | Service health check (Discord connection status) |
| `/alive` | GET | Basic availability check |

## Health Monitoring

- **`/alive`** - Always returns `yes` (service is running)
- **`/health`** - Returns `yes` if Discord bot is connected and ready, `no` otherwise

## Why Discord Resolver?

### The Problem
- **Discord removed direct user lookups** unless you share a server
- **No good self-hosted alternatives** existed

## How It Works

Discord Resolver leverages the **Discord Bot API**, which still allows bots to fetch user information by User ID. Unlike the regular user API, bot tokens can retrieve public user data without restrictions.

## Development

### Local Development
```bash
# Clone the repository
git clone https://github.com/your-repo/discord-resolver
cd discord-resolver

# Install dependencies
pip install -r requirements.txt

# Set environment variable
export DISCORD_TOKEN=your_bot_token_here

# Run the application
python main.py
```

The service will be available at `http://localhost:8080`

## Docker

### Build from Source
```bash
docker build -t discord-resolver .
docker run -p 8080:8080 -e DISCORD_TOKEN=<your_token> discord-resolver
```

## License

This project is licensed under GNU GPLv3.

---

