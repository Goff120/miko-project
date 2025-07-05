import discord
from discord.ext import commands
from discord import app_commands, Interaction
import json
import os
import asyncio

from guild_id import TARGET_GUILD
from gamble import BlackJack, Roulette

#interaction.user.id



class BlackEmbed(discord.ui.View):
    suit_emojis = {
        '♤': '♠️',
        '♡': '♥️',
        '♢': '♦️',
        '♧': '♣️',
    }

    def __init__(self, game: BlackJack, username: str):
        super().__init__(timeout=300)
        self.game = game
        self.username = username
        self.finished = False
        self.message = None

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        if self.message:
            try:
                print("turn off string 🤣")
                await self.message.edit(embed=self.display_hands(reveal_miko=False), view=self)
            except discord.HTTPException:
                pass

    def better_display(self, hand):
        output = ""
        for card in hand:
            if isinstance(card, str) and len(card) > 1:
                suit, num = card[-1], card[:-1]
                emoji = self.suit_emojis.get(suit, suit)
                output += f"**`{emoji} {num}`** "
        return output

    def display_hands(self, reveal_miko=False):
        info = self.game.info()
        embed = discord.Embed(
            title="🪙 Blackjack",
            description="**Miko is not responsible for your gambling addiction!!**",
            color=0x7851A9
        )

        # Miko (Dealer)
        if reveal_miko or self.finished:
            miko_hand = f"{self.better_display(info[2])} **` {info[3]} `**"
        else:
            miko_hand = f"{self.better_display([info[2][0]])} `❓❓`"
        embed.add_field(name="**Miko (Dealer)**", value=miko_hand, inline=False)

        # Player
        player_hand = f"{self.better_display(info[0])} **` {info[1]} `**"
        embed.add_field(name=f"**{self.username} (Player)**", value=player_hand, inline=False)

        if self.finished:
            result, box = self.game.check_winner()
            embed.add_field(name="**Result**", value=f"{result}\n\n\u2003{box}{self.game.bet_amount}", inline=False)

        return embed

    async def end_game(self, interaction: Interaction):
        self.finished = True
        for child in self.children:
            child.disabled = True

        user_id = interaction.user.id
        cog = interaction.client.get_cog("GambleCog")
        if cog and user_id in cog.active_games:
            del cog.active_games[user_id]

        final_embed = self.display_hands(reveal_miko=True)
        final_view = self
        final_view.add_item(self.replay_button(interaction.user.display_name))
        await interaction.message.edit(embed=final_embed, view=final_view)

    def replay_button(self, username):
        button = discord.ui.Button(label="Next game", style=discord.ButtonStyle.green, emoji="⏭️")

        async def callback(interaction: Interaction):
            await interaction.response.defer()
            user_id = interaction.user.id
            new_game = BlackJack()
            new_game.new_game(self.game.bet_amount)

            cog = interaction.client.get_cog("GambleCog")
            if cog:
                cog.active_games[user_id] = new_game

            for child in self.children:
                child.disabled = True

            if self.message:
                try:
                    await self.message.edit(view=self)
                except discord.HTTPException:
                    pass

            new_view = BlackEmbed(new_game, username)
            embed = new_view.display_hands()
            sent = await interaction.followup.send(embed=embed, view=new_view)
            new_view.message = sent

        button.callback = callback
        return button

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.blurple, emoji="🃏")
    async def hit_button(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.game.hit()
        if self.game.calculate_total(self.game.user_hand) > 21:
            await self.end_game(interaction)
        else:
            await interaction.message.edit(embed=self.display_hands(), view=self)

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.blurple, emoji="🖐️")
    async def stand_button(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.game.stand()
        await self.end_game(interaction)

    @discord.ui.button(label="Double Down", style=discord.ButtonStyle.green, emoji="🤑")
    async def double_button(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.game.double()
        self.game.stand()
        await self.end_game(interaction)


class GambleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}
        self.roulette = Roulette()

    @app_commands.guilds(TARGET_GUILD)
    @app_commands.command(name="blackjack", description="Play a round of Blackjack with Miko!")
    async def blackjack_command(self, interaction: Interaction, printer: int):
        await interaction.response.defer()

        user_id = interaction.user.id
        if user_id in self.active_games:
            del self.active_games[user_id]

        game = BlackJack()
        game.new_game(printer)
        self.active_games[user_id] = game

        view = BlackEmbed(game, interaction.user.display_name)
        embed = view.display_hands()
        await interaction.followup.send(embed=embed, view=view)

        view.message = await interaction.original_response()

    @app_commands.guilds(TARGET_GUILD)
    @app_commands.command(name="roulette", description="Miko thinks you should test your luck (gold.bet_type)")
    async def roulette_command(self, interaction: discord.Interaction, printer: str):
        response = self.roulette.roulette_bet(printer)
        if len(response) == 1:
            await interaction.response.send_message(str(response[0]), ephemeral=True)
        else:
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
        

            embed = discord.Embed(title="🪙Roulette", description="**Miko is not responsible for your gambling addiction!!**", color=0x7851A9)
            embed.set_image(url=gif)
            embed.add_field(name=message, value=add_on, inline=False)
            embed.add_field(name="Your bet:", value=printer, inline=True)
            embed.add_field(name="Result:", value=result, inline=True)
            embed.add_field(name="Colour:", value=colour, inline=True)
            embed.set_footer(text="finding gif that would work better is appreaticated")
            await interaction.response.send_message(embed=embed)
        self.bot.miko_used()

    @app_commands.guilds(TARGET_GUILD)
    @app_commands.command(name="look_see", description="Do you want Miko to give you pure gambling stats")
    async def look_see_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="✨Roulette Stats✨",
            color=0x008000,
            description= f"**Miko's love for numbers**\n\n")
        embed.description += str(self.roulette)
        await interaction.response.send_message(embed=embed)
        self.bot.miko_used()


async def setup(bot):
    await bot.add_cog(GambleCog(bot))