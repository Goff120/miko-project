# miko-project

## Discord Bot

This version of miko is stable and ready for use. It's a Raspberry Pi-hosted Discord bot designed for D&D campaigns to track PC information including deaths, kills, nat 20s, and nat 1s.

**Features:**
- AI-controlled NPCs with pre-made interactions
- Blackjack and roulette games with loss tracking
- Use `/help` for command documentation

> **Note:** Currently offline as the campaign has ended. Can be deployed if the code runs on the Pi.

## RL Miko

Currently in development with text-to-speech (TTS) and speech-to-text (STT) testing.

**Current Features:**
- Configurable weekly alarms with month-long scheduling
- Plays Spotify favorites or random songs instead of beeps
- Supports custom daily reminders

**Planned Features:**
- STT to stop alarms, favorite songs, and more
- TTS to deliver reminders before/after playback

## Pi Add-ons

**Audio & Microphone:**
- Any speaker with audio jack
- ReSpeaker Mic Array v2.0 (recommended for directional audio)

### Software

**For Discord Bot:**
```
discord.py
asyncio
psycopg2
openai
python-dotenv
```

**For RL Miko (Python 3.12.2):**
```bash
sudo apt update && sudo apt install -y build-essential libssl-dev zlib1g-dev \
    libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev \
    libgdbm-dev libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev tk-dev libffi-dev uuid-dev wget

wget https://www.python.org/ftp/python/3.12.2/Python-3.12.2.tgz
tar -xf Python-3.12.2.tgz && cd Python-3.12.2
./configure --enable-optimizations && make -j4 && sudo make altinstall
```

## Environment Variables

```
OPENAI_API_KEY=<your-openai-api-key>
DISCORD_TOKEN=<your-discord-bot-token>
SPOTIFY_CLIENT_ID=<your-spotify-client-id>
SPOTIFY_CLIENT_SECRET=<your-spotify-client-secret>
PLAYER1_ID=<discord-user-id>
PLAYER2_ID=<discord-user-id>
DB_HOST=localhost
DB_NAME=postgres
DB_USER=postgres
DB_PASS=<your-password>
```

## Contact

geoffreysmithuk@icloud.com
