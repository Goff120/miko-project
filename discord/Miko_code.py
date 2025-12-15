import discord
from discord.ext import commands
import json
import os
from datetime import datetime
import openai
from time import time
from dotenv import load_dotenv


from miko_speak import  MikoResponses
from guild_id import TARGET_GUILD

#chart order
#deaths
#kills
#natural 20
#natural 1

class MyClient(commands.Bot):

    name_order = (
            'Theos',
            'Herbert',
            'Otari',
            'Squeaker',
            'Kaela'
        )

    def __init__(self, command_prefix, intents, player_ids):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.absolute_admin = player_ids[0]
        self.miko_responses = MikoResponses(player_ids)

        self.data_file = "miko_Tamagotchi.json"
        self.last_miko_reply = {}
        self.miko_chat_history = []
        self.extra_happy = False
        self.mood = "neutral"
        self.id_to_character = {
            player_ids[0]: "Theos",
            player_ids[1]: "Herbert",
            player_ids[2]: "Otari",
            player_ids[3]: "Squeaker",
            player_ids[4]: "Kaela", 
            player_ids[5]: "GOD",
        }
        self.type = ["deaths","kills","luckys","unluckys","time"]

    async def setup_hook(self):
        try:
            guild = TARGET_GUILD  # Use the integer guild ID directly
            self.tree.clear_commands(guild=guild)
            
            await self.load_extension("silly")
            await self.load_extension("gambing_commands")
            await self.load_extension("character_stats") 
            await self.load_extension("admin")

            synced = await self.tree.sync(guild=guild)

            print(f"✅ Synced {len(synced)} command(s) to guild {guild.id}")
            for cmd in synced:
                print(f" - /{cmd.name}")

        except Exception as e:
            print(f"error syncing commands: {e}")

    async def on_ready(self):
        print(f"Hey hey hey it is your favorite bat {self.user}!!")

    def selection(self, title, stat_group):
        if title in ["deaths", "kills", "luckys", "unluckys"]:
            return self.name_order, stat_group
        elif title == "time":
            output = [
                stat_group[0]// 24, #days
                stat_group[0] % 24, #hours
                stat_group[1], #long rest
                stat_group[2]  #short rest
            ]
            return ["days", "hours", "long rest", "short rest"], output

    def output_stats(self, title):
        data = self.load_miko_data()
        stat_group = data[title]
        result = []

        selection_result = self.selection(title, stat_group)
        if selection_result is None:
            return ["No data available for this stat."]
        name_object, stat_group = selection_result

        for x in range(0, len(name_object)):
            output = f'{name_object[x]}: {stat_group[x]}'
            result.append(output)
        return result

    def load_miko_data(self):
        if not os.path.exists(self.data_file):
            print("finding file was to hard 😓")
            return {
                "fullness": 0,
                "last_fed": datetime.utcnow().isoformat(),
                "mood_points": 5,
                "last_played": datetime.utcnow().isoformat(),
                "items": [
                    "rat",
                    "sword",
                    "potion"
                ],
                "time": 0,
                "short_rest": 0,
                "long_rest": 0,
                "deaths": [0,0,0,0,0],
                "kills": [0,0,0,0,0],
                "luckys" : [0,0,0,0,0],
                "unluckys" : [0,0,0,0,0],
                "time": [0,0,0]
                }
        with open(self.data_file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("redoing homework with JSON 🙄")
                os.rename(self.data_file, f"{self.data_file}.bak")
                return self.load_miko_data()

    def save_miko_data(self, data):
        with open("miko_Tamagotchi.json", "w") as f:
            json.dump(data, f, indent=4)
            f.flush()
            os.fsync(f.fileno())

    def load_tables(self,table_path):
        try:
            with open(table_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"🙄 JSON broken in {table_path} — backing up and resetting.")
            os.rename(table_path, f"{table_path}.bak")
            return {}  
        except FileNotFoundError:
            print(f"⚠️ File {table_path} not found — creating new.")
            return {}

    def save_all(self):
        print("💾 Saving all tracked data...")

        try:
            miko_data = self.load_miko_data()
            self.save_miko_data(miko_data)
            print("✅ Miko data saved.")

        except Exception as e:
            print(f"❌ Error saving Miko data: {e}")

        try:
            roulette = self.load_tables("roulette_table.json")
            with open("roulette_table.json", "w") as f:
                json.dump(roulette, f, indent=4)
                f.flush()
                os.fsync(f.fileno())
            print("✅ roulette_table data saved.")

        except Exception as e:
            print(f"❌ Error saving roulette_table data: {e}")

    def decay_fullness(self, data):
        last_fed_time = datetime.fromisoformat(data["last_fed"])
        time_passed = datetime.utcnow() - last_fed_time
        days_passed = time_passed.total_seconds() / (60 * 60 * 24)
        decay = (100 / 7) * days_passed
        new_fullness = max(0, data["fullness"] - decay)
        self.extra_happy = True
        return int(new_fullness)

    def decay_mood(self, data):
        last_play_time = datetime.fromisoformat(data["last_played"])
        now = datetime.utcnow()
        
        midnight_last_played = datetime.combine(last_play_time.date(), datetime.min.time())
        midnight_now = datetime.combine(now.date(), datetime.min.time())
        
        days_passed = (midnight_now - midnight_last_played).days
        self.mood_points = max(0, data["mood_points"] - days_passed)
        return self.mood_points
    
    def miko_used(self):
        data = self.load_miko_data()
        _ = self.decay_mood(data) #exaple gets 5
        current_mood = max(0, min(10, self.mood_points + 1)) #example gets 6

        # Save updated data
        data["mood_points"] = current_mood
        data["last_played"] = datetime.utcnow().isoformat()
        self.save_miko_data(data)

    def find_mood(self): 
        if self.mood_points == 0:
            self.mood = "angry"
        elif self.mood_points < 2:
            self.mood = "sad"
        elif self.mood_points < 4:
            self.mood = "neutral"
        elif self.mood_points < 6:
            self.mood =  "happy"
        elif self.mood_points < 8:
            self.mood = "excited"
        elif self.mood_points < 10:
            self.mood = "ecstatic"
        
    def new_item(self, item):
        data = self.load_miko_data()
        items = data["items"]
        items.pop(0)
        items.append(item)
        data["items"] = items
        self.save_miko_data(data)
        self.extra_happy = True


    def change_chart(self, stat_type, character, num=1):
        print(f"Updating {stat_type}.{character} by {num}")
        data = self.load_miko_data()

        if stat_type == "time":
            try:
                if character == "Hours":
                    data["time"][0] += num
                elif character == "Long_rest":
                    data["time"][0] += 8
                    data["time"][1] += num
                elif character == "Short_rest":
                    data["time"][0] += 1
                    data["time"][2] += num
                elif character == "Days":
                    data["time"][0] += num * 24
            except ValueError:
                print(f"time unknown")
        else:
            try:
                index = self.name_order.index(character)
                data[stat_type][index] += num
            except ValueError:
                print(f"Character '{character}' not found.")
            
        self.save_miko_data(data)


    def generate_embed(self, row):
        titles = ["Deaths", "Kills", "Nat 20s", "Nat 1s", "Time"]
        descriptions = [
            "bozos getting knocked during the climax of the fight",
            "Wow you have been killing",
            "Come on come on Miko wants to see that nat 20",
            "Miko can always edit that out, we ain't live",
            "Miko is not a clock, but Miko can tell you the time"
        ]
        colors = [0xffffff, 0xca3631, 0xFFD700, 0x665a2c,0xE89EB8]

        stats = self.output_stats(self.type[row])
        embed = discord.Embed(title=titles[row], description=descriptions[row], color=colors[row])
        
        for stat in stats:
            embed.add_field(name=stat, value=" ", inline=False)
        

        return embed

    def persentage(self,current):
        percent = round((current / 100) * 100)
        bar = "█" * (percent // 10) + "░" * (10 - percent // 10)
        return bar,percent
    
    #---------------
    #AI part of Miko
    #---------------

    async def on_message(self,message: str): 
        #no chat chat to self
        if message.author == self.user:
            return

        # Only respond in the talk-to-miko channel
        if message.channel.id == 1374723262117838879:  #talk channel ID
            self.miko_used()
            data = self.load_miko_data()

            if self.extra_happy:
                self.mood = "EUPHORIC"
                self.extra_happy = False
            else:
                self.find_mood()

            userid = message.author.id
            player = self.id_to_character.get(userid, "unknown")


            now = time()
            last_time = self.last_miko_reply.get(message.author.id, 0)
            if now - last_time < 5:
                await message.channel.send("Miko is busy... he just found a new snack in your pockets! 🍪")
                return #shut up chatty box users

            self.last_miko_reply[message.author.id] = now

            system_msg = {
                "role": "system",
                "content": (
                    "You are Miko, a small, sassy, bat-like drone assistant"
                    "who records a D&D party. he speak in third person, bit dramatic."
                    f"mood {self.mood}"
                    f"items: {data['items']}"
                    f"you are talking to {player}"
                    f"your fullness is {data['fullness']}%"
                )
            }
            user_msg = {"role": "user", "content": message.content}
            chat_history = self.miko_chat_history[-3:]  # he has short term memory of 3 messages
            ask = [system_msg] + chat_history + [user_msg]
            try:
                await message.channel.typing()

                if message.content.startswith('+'):
                    using_mode = "gpt-4-turbo"
                    print("turbo")
                else:
                    using_mode = "gpt-3.5-turbo"

                response = ai_client.chat.completions.create(
                    model=using_mode,
                    messages = ask,
                    max_tokens=100,
                    temperature=0.8
                )

                reply = response.choices[0].message.content

                self.miko_chat_history.append(user_msg)
                self.miko_chat_history.append({"role": "assistant", "content": reply})
                self.miko_chat_history = self.miko_chat_history[-6:]

                await message.channel.send(reply.strip())

            except Exception as e:
                await message.channel.send("Miko is confused... and Miko's brain isn't responding 😖")
                print(f"[Miko AI error] {e}")

        await self.process_commands(message)




intent = discord.Intents.default()
intent.message_content = True

load_dotenv()
player_ids = [int(os.getenv(f"PLAYER{i}_ID")) for i in range(1, 8)]

client = MyClient(command_prefix='!', intents=intent, player_ids=player_ids)
guild = TARGET_GUILD

api_key = os.getenv("OPENAI_API_KEY")
ai_client = openai.OpenAI(api_key=api_key)

token = os.getenv("DISCORD_TOKEN")
client.run(token)

#py Miko_code.py