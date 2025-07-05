import discord
from discord.ext import commands
from discord import app_commands, Interaction
import asyncio

from guild_id import TARGET_GUILD


class ChartView(discord.ui.View):
    def __init__(self, row_to_update: int, button_set: list[tuple], client_ref: "MyClient", mode="chart", message: discord.Message = None, alowed_button=False):
        super().__init__(timeout=None)
        self.row = row_to_update
        self.client = client_ref
        self.message = message
        self.mode = mode  
        self.button_set = button_set

        if alowed_button:
            for label, emoji, action in button_set:
                self.add_item(self.make_button(label, emoji, action))

            self.add_item(self.make_reload_button())

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
                self.client.change_chart(self.client.type[self.row], target)
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

class StatsCog(commands.Cog):
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

    def __init__(self, bot):
        self.bot = bot
        

    @app_commands.guilds(TARGET_GUILD)
    @app_commands.command(name="deaths", description="Miko can tell your deaths")
    async def deaths_command(self, interaction: Interaction):
        embed = self.bot.generate_embed(0)

        alowed_button = False
        if self.bot.absolute_admin == interaction.user.id:
            alowed_button = True

        await interaction.response.send_message(embed=embed, view=ChartView(0, self.player_buttons, self.bot, mode="chart",alowed_button = alowed_button))

    @app_commands.guilds(TARGET_GUILD)
    @app_commands.command(name="kills", description="Die die die")
    async def kills_command(self, interaction: Interaction):
        embed = self.bot.generate_embed(1)

        alowed_button = False
        if self.bot.absolute_admin == interaction.user.id:
            alowed_button = True

        await interaction.response.send_message(embed=embed, view=ChartView(1, self.player_buttons, self.bot, mode="chart",alowed_button = alowed_button))
        self.bot.miko_used()

    @app_commands.guilds(TARGET_GUILD)
    @app_commands.command(name="luckys", description="Now how lucky have you all been")
    async def luckys_command(self, interaction: Interaction):
        embed = self.bot.generate_embed(2)

        alowed_button = False
        if self.bot.absolute_admin == interaction.user.id:
            alowed_button = True

        await interaction.response.send_message(embed=embed, view=ChartView(2, self.player_buttons, self.bot, mode="chart",alowed_button = alowed_button))
        self.bot.miko_used()

    @app_commands.guilds(TARGET_GUILD)
    @app_commands.command(name="unluckys", description="Aww man it is just not ya day now")
    async def unluckys_command(self, interaction: Interaction):
        embed = self.bot.generate_embed(3)

        alowed_button = False
        if self.bot.absolute_admin == interaction.user.id:
            alowed_button = True

        await interaction.response.send_message(embed=embed, view=ChartView(3, self.player_buttons, self.bot, mode="chart",alowed_button = alowed_button))
        self.bot.miko_used()

    @app_commands.guilds(TARGET_GUILD)
    @app_commands.command(name="time", description="Sometime the party needs sometime")
    async def time_command(self, interaction: Interaction):
        embed = self.bot.generate_embed(4)

        alowed_button = False
        if self.bot.absolute_admin == interaction.user.id:
            alowed_button = True

        await interaction.response.send_message(embed=embed, view=ChartView(4, self.time_buttons, self.bot, mode="time",alowed_button = alowed_button))
        self.bot.miko_used()  

    @app_commands.guilds(TARGET_GUILD)
    @app_commands.command(name="hours", description="when time flys")
    async def hours_command(self, interaction: Interaction, printer: str):
        
        try:
            num = int(printer)
            self.bot.change_chart("time", "Hours", num=num)
            await interaction.response.send_message(f"Miko has added {num} hours!", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("Miko tilts his head... error happened! 😖", ephemeral=True)


async def setup(bot):
    await bot.add_cog(StatsCog(bot))