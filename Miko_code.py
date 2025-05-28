import discord
from discord.ext import commands
import json
from random import choice
import os
from datetime import datetime
import openai
from time import time
from dotenv import load_dotenv
import asyncio

from gamble import Roulette


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
    
    types = (
            "deaths",
            "kills",
            "luckys",
            "unluckys",
            "time"
        )

    def __init__(self, command_prefix, intents,player_ids):
        super().__init__(command_prefix=command_prefix, intents=intents)
        
        self.data_file = "miko_Tamagotchi.json"
        self.last_miko_reply = {}
        self.miko_chat_history = []
        self.extra_happy = False
        self.mood = "neutral"

        self.id_to_character = {
            player_ids[0] : "Theos",
            player_ids[1] : 'Herbert',
            player_ids[2] : 'Otari',
            player_ids[3] : 'Squeaker',
            player_ids[4] : 'Kaela',
            player_ids[5] : 'GOD',
    }
        

    async def on_ready(self):
        print(f'Hey hey hey it is your favorite bat {self.user}!!')

        try:
            guild= discord.Object(id = 1101519682583941121)
            synced = await self.tree.sync(guild=guild) 
            print(f'Synced {len(synced)} command(s) to guild {guild.id}.')
            #await self.tree.sync(guild=guild)
            #await self.tree.clear_commands(guild=guild)
            #await self.tree.sync(guild=guild)

        except Exception as e:
            print(f'Error syncing commands: {e}')

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
        stat_group = data[title] #example gets 0,0,0,0,0
        result = []


        name_object, stat_group= self.selection(title,stat_group)   

        for x in range (0, len(name_object)):
            output = f'{name_object[x]}: {stat_group[x]}'
            result.append(output)
        return result

    def load_miko_data(self):
        if not os.path.exists(self.data_file):
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
            return json.load(f)

    def save_miko_data(self, data):
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=4)

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
        data = client.load_miko_data()
        _ = client.decay_mood(data) #exaple gets 5
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

        stats = self.output_stats(self.types[row])
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
        if message.author == client.user:
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

#-----------------------
# buttons for the charts
#-----------------------  
  
class ChartView(discord.ui.View):
    def __init__(self, row_to_update: int, button_set: list[tuple], client_ref: MyClient, mode="chart", message: discord.Message = None):
        super().__init__(timeout=None)
        self.row = row_to_update
        self.client = client_ref
        self.message = message
        self.mode = mode  
        self.button_set = button_set

        for label, emoji, action in button_set:
            self.add_item(self.make_button(label, emoji, action))

        self.add_item(self.make_reload_button())

    def make_button(self, label, emoji, target):
        button = discord.ui.Button(
            label=label,
            style=discord.ButtonStyle.blurple,
            emoji=emoji
        )

        async def button_callback(interaction: discord.Interaction):
            if self.mode == "chart":
                self.client.change_chart(self.client.types[self.row], target)
            elif self.mode == "time":
                self.client.change_chart("time", target)
            
            await self.update_message(interaction)
            await interaction.response.defer()

        button.callback = button_callback
        return button

    async def update_message(self, interaction: discord.Interaction):
        embed = self.client.generate_embed(self.row)
        await interaction.message.edit(embed=embed, view=self)
    
    def make_button(self, label, emoji, target):
        button = discord.ui.Button(
            label=label,
            style=discord.ButtonStyle.blurple,
            emoji=emoji
        )

        async def button_callback(interaction: discord.Interaction):
            if self.mode == "chart":
                self.client.change_chart(self.client.types[self.row], target)
            elif self.mode == "time":
                self.client.change_chart("time", target)
            
            await self.update_message(interaction)
            await interaction.response.defer()

        button.callback = button_callback
        return button

    def make_reload_button(self):
        button = discord.ui.Button(
            label="Reload",
            style=discord.ButtonStyle.red,
            emoji="🔄"
        )

        async def reload_callback(interaction: discord.Interaction):
            await interaction.response.defer(thinking=True)

            try:
                message = interaction.message
                new_embed = self.client.generate_embed(self.row)  
                await message.edit(embed=new_embed)
                msg = await interaction.followup.send("Miko refreshed the stats! 📊✨", ephemeral=True, wait=True)
                await asyncio.sleep(5)
                await msg.delete()

            except Exception as e:
                msg = await interaction.followup.send("Miko choked while reloading... 😵 Error: {e}", ephemeral=True, wait=True)
                await asyncio.sleep(5)
                await msg.delete()

                
        button.callback = reload_callback
        return button
    
#-------------------------
#responses for Miko to say   
#------------------------- 

class MikoResponses():
    def __init__(self,player_id):
        self._say_hello = {
            player_id[0] : "Hey Theos, doing well hunting?⚔️",
            player_id[1] : 'what are you up to Herbert? 🥰',
            player_id[2] : 'pls don eat me Otari 😱',
            player_id[3] : 'hi Squeaker, do you wana play some games?🏉',
            player_id[4] : 'what up, Miko was wordering what you are making Kaela?🧐',
            player_id[5] : "*squeaks in fear* Miko can't handle this!😨",
            player_id[6] : 'Miko does not know you!!! Go away! 😫',
        }

        #----------------
        #status responses
        #----------------

        self._low_status = [
            "Miko is a hollow husk... abandoned... 😭",
            "*pathetic squeak*... Miko fears the end is near.",
            "He wraps himself in his wings and sighs dramatically.",
            "Miko gnaws on a table leg. It's come to this."
        ]

        self._low_mid_status = [
            "Miko tilts his head hopefully. Any scraps... maybe?",
            "*tiny hopeful squeak*... you wouldn't forget Miko, right?",
            "He pokes your bag looking for snacks.",
            "Miko hovers, trying not to look desperate (failing)."
        ]

        self._mid_status = [
            "Miko squeaks happily, belly full and heart lighter!",
            "He twirls in the air like a fluffy bat-top. 🎶",
            "Miko pats his tummy contentedly and winks.",
            "He lounges dramatically, satisfied beyond reason."
        ]

        self._full_excited_status = [
            "Miko zooms in circles, squeaking joyfully!",
            "He chirps at random passersby, showing off his fullness.",
            "Miko does a midair somersault. Because he can.",
            "He hurls tiny crumbs at you in triumph. 🦇✨"
        ]

        self._overfull_euphoric_status = [
            "Miko is vibrating with bliss. Nothing can touch him now.",
            "He lies on his back, wings spread, whispering about destiny.",
            "Miko believes he could defeat a dragon. Or take a nap. Either one.",
            "He giggles uncontrollably between tiny hiccups."
        ]

        #----------------
        #hunger responses
        #----------------

        self._low_hunger = [
            "Miko looks starved... 🥺",
            "*weak squeak*... you remembered me...",
            "He clings to your leg like you’re his last hope."
        ]

        self._mid_hunger = [
            "Miko accepts your offering with a happy squeak.",
            "*nom nom nom* 🦇",
            "He chirps gratefully and curls up nearby."
        ]

        self._full_hunger = [
            "He nibbles politely. He’s already pretty stuffed.",
            "He blinks slowly. Not hungry... but okay.",
            "Miko eats it anyway. He's a little piggy today."
        ]

        self._rare_hunger = [
            "Miko refuses. He's in his mysterious phase.",
            "He flips the food over. Rude but elegant.",
            "He demands snacks *AND* drama."
        ]

        self._help_embed = {
            "Party stats" :
            "Commands: `/deaths` `/kills` `/luckys` `/unluckys`\n"\
            "Miko will show how your campaign is progressing.\n"\
            "You can either:\n"
            "Use the buttons to increment each player's count by 1, or\n"\
            "Use the `/fix` command with the format type.character.num \n"\
            "After using a `/fix` command, you’ll need to press the reload button to see the updated values.",
        
            "Time" :
            "The `/time` command works similarly but displays the time for days, hours, and rests.\n"\
            "Use `/hours` to add time based on what you input.\n"\
            "`/fix` also works doing \ntime.hours.num, time.short_rest.num, time.long_rest.num",

            "Fix":
            "In `/fix` the num will be negative by default\n"\
            "You can use `/fix` to increase values by inputting a negative number",

            "Tamagotchi":
            "Miko needs to be fed and talked to regularly.\n"\
            "Using almost any command increases Miko’s happiness.\n\n"\
            "To feed him, use `/feed_miko` and give him a snack.\n"\
            "To check how Miko is doing, use `/status`.\n\n"\
            "You can also give Miko up to three items using the command:\n"\
            "/give_miko then teh item you want to give.",

        
            "Gamble":
            "You can currently play roulette using the `/roulette` command.\n"\
            "Place bets using the format gold.bet_type.\n"\
            "Available types include: \nred, black, even, odd, low, high, 1st12, 2nd12,3rd12\n"\
            "You can also bet on single or multiple numbers.\n"\
            "For multiple numbers, use a format like 400.13_18.\n"\
            "To see what's currently popular on the table, use `/look_see`.\n\n"\
            "Note: The GIFs are currently not working well.\n"\
            "Miko uses the Eurpean wheel so no 00",

            
            "Chat":
            "You can talk to Miko directly in the #talk-to-miko channel.\n"
            "If you start your message with a `+`, Miko will respond more intelligently.\n"\
            "Example: +How are you today, Miko?"
        }

    def status_response(self, status_level):
        if status_level >= 0.9:
            return choice(self._overfull_euphoric_status)
        elif status_level >= 0.7:
            return choice(self._full_excited_status)
        elif status_level >= 0.4:
            return choice(self._mid_status)
        elif status_level >= 0.2:
            return choice(self._low_mid_status)
        else:
            return choice(self._low_status)
        
    def hunger_response(self, hunger_level):
        if hunger_level < 20:
            return choice(self._low_hunger)
        elif hunger_level < 40:
            return choice(self._low_hunger)
        elif hunger_level < 70:
            return choice(self._mid_hunger)
        elif hunger_level < 90:
            return choice(self._full_hunger)
        else:
            return choice(self._rare_hunger)
        
    def get_help_field(self, title):
        try:
            field = {
                "name": f"*{title}*",
                "value": self._help_embed[title],
                "inline": False
            }
            return field
        except KeyError:
            raise ValueError('That is not a valid title for help')
        
    @property
    def say_hello(self):
        return self._say_hello

#idk why they need to be here but they do
#----------------------------------------------------
intent = discord.Intents.default()
intent.message_content = True
load_dotenv()
player_ids = [int(os.getenv(f"PLAYER{i}_ID")) for i in range(1, 7)]
client = MyClient(command_prefix='!', intents=intent, player_ids=player_ids)
guild = discord.Object(id=1101519682583941121)
#----------------------------------------------------

#---------------------------------------
#important info the main task of the bot
#---------------------------------------
@client.tree.command(name="deaths", description="Miko can tell your deaths", guild=guild)
async def deaths_command(interaction: discord.Interaction):
    embed = client.generate_embed(0)
    await interaction.response.send_message(embed=embed, view=ChartView(0, player_buttons, client, mode="chart"))

@client.tree.command(name="kills", description="Die die die", guild=guild)
async def kills_command(interaction: discord.Interaction):
    embed = client.generate_embed(1)
    await interaction.response.send_message(embed=embed, view=ChartView(1, player_buttons, client, mode="chart"))
    client.miko_used()

@client.tree.command(name="luckys", description="Now how lucky have you all been", guild=guild)
async def luckys_command(interaction: discord.Interaction):
    embed = client.generate_embed(2)
    await interaction.response.send_message(embed=embed, view=ChartView(2, player_buttons, client, mode="chart"))
    client.miko_used()

@client.tree.command(name="unluckys", description="Aww man it is just not ya day now", guild=guild)
async def unluckys_command(interaction: discord.Interaction):
    embed = client.generate_embed(3)
    await interaction.response.send_message(embed=embed, view=ChartView(3, player_buttons, client, mode="chart"))
    client.miko_used()

@client.tree.command(name="time", description="Sometime the party needs sometime", guild=guild)
async def time_command(interaction: discord.Interaction):
    embed = client.generate_embed(4)
    await interaction.response.send_message(embed=embed, view=ChartView(4, time_buttons, client, mode="time"))
    client.miko_used()

@client.tree.command(name="fix", description="Fix data using type.character.num", guild=guild)
async def fix_command(interaction: discord.Interaction, printer: str):

    selction = printer.split(".")
    
    type = selction[0].lower()
    character = selction[1].lower().capitalize()
    num = -int(selction[2])

    try:
        await interaction.response.defer(ephemeral=True)
        client.change_chart(type, character, num=num)
        message = await interaction.original_response()

        row = client.types.index(type)
        embed = client.generate_embed(row)
         
        for field in embed.fields:
            if field.name.startswith(character):
                old_value = int(field.name.split(":")[1].strip())
                new_value = old_value + num
                field.name = f"{character}: {new_value}"
                break

        await message.edit(embed=embed)
        await interaction.followup.send("Miko has updated the chart! 🛠️", ephemeral=True)

    except Exception as e:
        await interaction.response.send_message(
            f"Miko tilts his head... error happened! 😖 {e}",
            ephemeral=True
        )

@client.tree.command(name="hours", description="when time flys", guild=guild)
async def hours_command(interaction: discord.Interaction, printer: str):
    
    try:
        num = int(printer)
        client.change_chart("time", "Hours", num=num)
        await interaction.response.send_message(f"Miko has added {num} hours!", ephemeral=True)
    except ValueError:
        await interaction.response.send_message("Miko tilts his head... error happened! 😖", ephemeral=True)




#---------------------------------
#extra silly things for Miko to do
#---------------------------------
@client.tree.command(name="hello", description="Say hello to Miko", guild=guild)
async def hello_command(interaction: discord.Interaction):
    username = interaction.user.id
    response = miko_responses.say_hello.get(username, "Miko does not know you!")
    await interaction.response.send_message(response)
    client.miko_used()

@client.tree.command(name="give_miko", description="Give Miko an Item", guild=guild)
async def give_miko(interaction: discord.Interaction, printer:str):
    await interaction.response.send_message(f"Miko received a {printer}!")
    sent = await interaction.original_response()
    await sent.add_reaction("🥰")
    client.new_item(printer)
    client.miko_used()

@client.tree.command(name="feed_miko", description="This guy gets hungry too", guild=guild)
async def feed_miko(interaction: discord.Interaction):

    data = client.load_miko_data()
    current_fullness = client.decay_fullness(data) #exaple gets 53
    current_fullness = min(100, current_fullness + 25) #example gets 78

    bar, percent = client.persentage(current_fullness)
    #how much is Miko's hunger

    # Save updated data
    data["fullness"] = current_fullness
    data["last_fed"] = datetime.utcnow().isoformat()
    client.save_miko_data(data)

    # Pick response flavor
    flavor = miko_responses.hunger_response(current_fullness)
    

    # Combine bar and flavor into one message
    message_text = f"**Miko's Fullness**\n{bar} {percent}%\n\n{flavor}"
    await interaction.response.send_message(message_text)

    sent = await interaction.original_response()
    await sent.add_reaction("🥰")
    client.miko_used()

@client.tree.command(name="status", description="sometime you just have to check how your friend is doing", guild=guild)
async def miko_status(interaction: discord.Interaction):
    data = client.load_miko_data()
    current_fullness = client.decay_fullness(data)
    current_mood = client.decay_mood(data)
    print(current_mood)

    #use the blank part div by 100 and time them, toghere to get better status
    bar, full_per = client.persentage(current_fullness)
    bar2, mood_per = client.persentage(current_mood*10)

    full_per = full_per / 100
    mood_per = mood_per / 100

    status_level = (full_per + mood_per) /2

    item_list = data["items"]

    embed = discord.Embed(
        title="Miko's Status",
        color=0x5D3FD3,
        description= f'{miko_responses.status_response(status_level)}\n\n'
        f"**Miko's Fullness**\n{bar} {current_fullness}%\n\n"
        f"**Miko's Mood**\n{bar2} {current_mood*10}%\n\n"
        f"**Miko's Items**\n{', '.join(item_list)}\n\n"
        )
    await interaction.response.send_message(embed=embed)

#-------------------
#gambel part of Miko
#-------------------

####fix the gifssssss
@client.tree.command(name="roulette", description="Miko thinks you should test your luck (gold.bet_type)", guild=guild)
async def roulette_command(interaction: discord.Interaction, printer: str):
    response = roulette.roulette_bet(printer)
    message = response[0]
    gif = response[1]
    win_lose = response[2]
    colour = response[3]
    result = response[4]
    gold = response[5]

    if win_lose:
        add_on = f"Miko is happy for you! \n\n\u2003🟩 {gold}"
    else:
        add_on = f"Miko is sad for you... \n\n\u2003🟥 {gold}"
    
    if gif is None:
        await interaction.response.send_message(str(message), ephemeral=True)
    else:
        embed = discord.Embed(title="🪙Roulette", description="**Miko is not responsible for your gambling addiction!!**", color=0x7851A9)
        embed.set_image(url=gif)
        embed.add_field(name=message, value=add_on, inline=False)
        embed.add_field(name="Your bet:", value=printer, inline=True)
        embed.add_field(name="Result:", value=result, inline=True)
        embed.add_field(name="Colour:", value=colour, inline=True)
        embed.set_footer(text="finding gif that would work better is appreaticated")
        await interaction.response.send_message(embed=embed)
    client.miko_used()

@client.tree.command(name="look_see", description="Do you want Miko to give you pure gambling stats", guild=guild)
async def miko_look_see(interaction: discord.Interaction):
    embed = discord.Embed(
        title="✨Roulette Stats✨",
        color=0x008000,
        description= f"**Miko's love for numbers**\n\n")
    embed.description += str(roulette)
    await interaction.response.send_message(embed=embed)
    client.miko_used()


    

@client.tree.command(name="help", description="ask for help only one thing? use: Party stats, Time, Fix, Tamagotchi, Gamble, Chat", guild=guild)
async def help_command(interaction: discord.Interaction, printer:str = None):
    
    embed = discord.Embed(
        title="Miko's Help",
        color=0xf2ce94,
        description="**Miko is here to help you!**\n\n"
    )
    if printer is None:
        embed.add_field(**miko_responses.get_help_field("Party stats"))
        embed.add_field(**miko_responses.get_help_field("Time"))
        embed.add_field(**miko_responses.get_help_field("Fix"))
        embed.add_field(**miko_responses.get_help_field("Tamagotchi"))
        embed.add_field(**miko_responses.get_help_field("Gamble"))
        embed.add_field(**miko_responses.get_help_field("Chat"))
    else:
        try:
            embed.add_field(**miko_responses.get_help_field(printer.lower().capitalize()))
        except (IndexError) as problem:
            await interaction.response.send_message('error:',str(problem))
    await interaction.response.send_message(embed=embed)

#add more stuff to interact with the bot here




player_ids += [int(os.getenv("PLAYER7_ID"))]#annoying extra non player id
miko_responses = MikoResponses(player_ids)
roulette = Roulette()


api_key = os.getenv("OPENAI_API_KEY")
ai_client = openai.OpenAI(api_key=api_key)

player_buttons = [
    ("Theos", "🐰", "Theos"),
    ("Herbert", "👨🏻‍🦳", "Herbert"),
    ("Otari", "🦁", "Otari"),
    ("Squeaker", "🐦‍⬛", "Squeaker"),
    ("Kaela", "🗑️", "Kaela"),
]

time_buttons = [
    ("Add Day", "🌞", "Days"),        
    ("Add Hour", "⏰", "Hours"),        
    ("Long Rest", "🛌", "Long_rest"),       
    ("Short Rest", "🔥", "Short_rest"),      
]


#ping_buttons = [
    #("Theos", "🐰", "Theos"),
    #("Herbert", "👨🏻‍🦳", "Herbert"),
    #("Otari", "🦁", "Otari"),
    #("Squeaker", "🐦‍⬛", "Squeaker"),
    #("Kaela", "🗑️", "Kaela"),
#]
token = os.getenv("DISCORD_TOKEN")
client.run(token)

#py Miko_code.py