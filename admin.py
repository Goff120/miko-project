import discord
from discord.ext import commands
from discord import app_commands, Interaction
import json
import os

from guild_id import TARGET_GUILD, TARGET_CHANNEL

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(TARGET_GUILD)
    @app_commands.command(name="fix", description="Fix data using type.character.num")
    async def fix_command(self, interaction: discord.Interaction, printer: str):

        selction = printer.split(".")
        
        type = selction[0].lower()
        character = selction[1].lower().capitalize()
        num = -int(selction[2])

        try:
            await interaction.response.defer(ephemeral=True)
            self.bot.change_chart(type, character, num=num)
            message = await interaction.original_response()

            row = self.bot.types.index(type)
            embed = self.bot.generate_embed(row)
            
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


    @app_commands.guilds(TARGET_GUILD)
    @app_commands.command(name="help", description="ask for help only one thing? use: Party stats, Time, Fix, Tamagotchi, Gamble, Chat")
    async def help_command(self, interaction: Interaction, printer:str = None):
        
        embed = discord.Embed(
            title="Miko's Help",
            color=0xf2ce94,
            description="**Miko is here to help you!**\n\n"
        )
        if printer is None:
            embed.add_field(**self.bot.miko_responses.get_help_field("Party stats"))
            embed.add_field(**self.bot.miko_responses.get_help_field("Time"))
            embed.add_field(**self.bot.miko_responses.get_help_field("Fix"))
            embed.add_field(**self.bot.miko_responses.get_help_field("Tamagotchi"))
            embed.add_field(**self.bot.miko_responses.get_help_field("Gamble"))
            embed.add_field(**self.bot.miko_responses.get_help_field("Chat"))
        else:
            try:
                embed.add_field(**self.bot.miko_responses.get_help_field(printer.lower().capitalize()))
            except (IndexError) as problem:
                await interaction.response.send_message(f'error: {problem}')
        await interaction.response.send_message(embed=embed)

    
    @app_commands.guilds(TARGET_GUILD)
    @app_commands.command(name="shutdown", description="miko is getting a restart or upgrade of some kind")
    async def shutdown_command(self, interaction: Interaction):
        await interaction.response.defer()
        if self.bot.absolute_admin == interaction.user.id:
            self.bot.save_all()

            try:
                channel = self.bot.get_channel(TARGET_CHANNEL)
                if channel and isinstance(channel, discord.TextChannel):
                    def not_pinned(msg):
                        return not msg.pinned
                    await channel.purge(limit=None, check=not_pinned)
                    print("🧹 Channel messages cleared.")
            except Exception as e:
                print(f"❌ Error clearing channel: {e}")


            await interaction.followup.send("Miko shutdown done, see you later all")
            await self.bot.close()

            
        else:
            await interaction.followup.send("Oi you have no right 😠")


async def setup(bot):
    await bot.add_cog(AdminCog(bot))