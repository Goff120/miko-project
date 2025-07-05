import discord
from discord.ext import commands
from discord import app_commands, Interaction
from datetime import datetime

from guild_id import TARGET_GUILD

class SillyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(TARGET_GUILD)
    @app_commands.command(name="hello", description="Say hello to Miko")
    async def hello_command(self, interaction: Interaction):
        username = interaction.user.id
        response = self.bot.miko_responses.say_hello.get(username, "Miko does not know you!")
        await interaction.response.send_message(response)
        self.bot.miko_used()

    @app_commands.guilds(TARGET_GUILD)
    @app_commands.command(name="give_miko", description="Give Miko an Item")
    async def give_miko_command(self, interaction: Interaction, printer: str):
        await interaction.response.send_message(f"Miko received a {printer}!")
        sent = await interaction.original_response()
        await sent.add_reaction("🥰")
        self.bot.new_item(printer)
        self.bot.miko_used()

    @app_commands.guilds(TARGET_GUILD)
    @app_commands.command(name="feed_miko", description="This guy gets hungry too")
    async def feed_miko_command(self, interaction: Interaction):
        data = self.bot.load_miko_data()
        current_fullness = self.bot.decay_fullness(data)
        current_fullness = min(100, current_fullness + 25)

        bar, percent = self.bot.persentage(current_fullness)

        data["fullness"] = current_fullness
        data["last_fed"] = datetime.utcnow().isoformat()

        self.bot.save_miko_data(data)
        self.bot.save_miko_data(data)

        flavor = self.bot.miko_responses.hunger_response(current_fullness)

        message_text = f"**Miko's Fullness**\n{bar} {percent}%\n\n{flavor}"
        await interaction.response.send_message(message_text)

        sent = await interaction.original_response()
        await sent.add_reaction("🥰")
        self.bot.miko_used()

    @app_commands.guilds(TARGET_GUILD)
    @app_commands.command(name="status", description="Check how your friend is doing")
    async def status_command(self, interaction: Interaction):
        data = self.bot.load_miko_data()
        current_fullness = self.bot.decay_fullness(data)
        current_mood = self.bot.decay_mood(data)

        bar, full_per = self.bot.persentage(current_fullness)
        bar2, mood_per = self.bot.persentage(current_mood * 10)

        full_per = full_per / 100
        mood_per = mood_per / 100

        status_level = (full_per + mood_per) / 2
        item_list = data.get("items", [])

        embed = discord.Embed(
            title="Miko's Status",
            color=0x5D3FD3,
            description=(
                f'{self.bot.miko_responses.status_response(status_level)}\n\n'
                f"**Miko's Fullness**\n{bar} {current_fullness}%\n\n"
                f"**Miko's Mood**\n{bar2} {current_mood * 10}%\n\n"
                f"**Miko's Items**\n{', '.join(item_list) if item_list else 'None'}\n\n"
            )
        )
        await interaction.response.send_message(embed=embed)

    

async def setup(bot):
    await bot.add_cog(SillyCog(bot))