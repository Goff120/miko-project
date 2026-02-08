# miko-project

## discord bot
this version of miko is useable and in a state i am currently happy with using
miko is a raspberry PI hosted bot for some dnd fun and is mainly used to track infomation about each PC such as deaths kills nat 20s and nat 1s. 

miko also hads features to make an npc that is not controled by the DM but AI and pre made interations.

miko had some dumb fun that was requested i make of blackjack and roulette that scores the individual on how badly they have lost 

for more info on how to use the command you can do /help when he is running on the server 
(ps miko can just be added and should work if the code is running on my PI)
(currently not running as the campain i was playing ended and i have not joined the current one)

## RL miko
it is not functional as i had to stop due to work and uni life :( 
currently in testing of how i would make tts and stt 

what is there tho is an alarm you can set for of the week able to make a full months set of alarms for individual days 

insead of the soul sucking beeps miko would get your favs or a random song from spotify to play 

future with the test for tts and stt
the alarm would use stt to stop the alarm fav the song that he is playing and a few other things 
for tts the alarm can hold infomation that it tells the user before and after the song so you can include normal very day reminders (god i need this)

## the PIs add ons
things i use to work with my pi
for aduio i would use any speaker with an audio jack 
the microphone i would use anything that is cable but i use ReSpeaker Mic Array v2.0 as it has fun light and mics to tell where i am in the room 

### software 
if you want just discord the python3 pre built should just work well  
the libarys used and install:
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
