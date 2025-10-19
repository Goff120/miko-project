import discord
from discord.ext import commands
from discord import app_commands, Interaction
from dotenv import load_dotenv
import os
import psycopg2

from guild_id import TARGET_GUILD
from gamble import BlackJack, Roulette

#interaction.user.id

class SqlData(commands.Cog):

    def __init__ (self):
        load_dotenv()
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"))
        self.cur = self.conn.cursor()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS discord_user (
            id SERIAL PRIMARY KEY,
            discord_id BIGINT NOT NULL UNIQUE,
            name VarChar(33),
            won INT,
            lost INT,
            played_games INT
        );
        """)
    


    def if_new(self, interaction: discord.Interaction):
        discord_id = interaction.user.id
        discord_name = interaction.user.name

        try:
            self.cur.execute(
            """INSERT INTO discord_user (discord_id, name, won, lost, played_games) VALUES
            (%s, %s, 0, 0, 0) ON CONFLICT (discord_id) DO NOTHING;""",
            (discord_id, discord_name)
            )
            self.conn.commit()
        except Exception as e:
            print(f"Error inserting user: {e}")

    def win_gold(self, gold, interaction: discord.Interaction):
        discord_id = interaction.user.id

        self.cur.execute("""
            SELECT won, played_games
            FROM discord_user 
            WHERE discord_id = %s
        """, (discord_id,))

        result = self.cur.fetchone()
        if result is None:
            self.if_new(interaction)

            new_played_games = 1
            current_won = 0

        else:
            current_won = result[0] if result and result[0] is not None else 0
            cur_played_games = result[1] if result and result[1] is not None else 0

            new_played_games = cur_played_games + 1

        new_won = current_won + gold

        self.cur.execute("""
            UPDATE discord_user
            SET won = %s, played_games = %s
            WHERE discord_id = %s
        """, (new_won,new_played_games, discord_id))
        
        self.conn.commit()

    def lose_gold(self, gold, interaction: discord.Interaction):
        discord_id = interaction.user.id

        self.cur.execute("""
            SELECT lost, played_games
            FROM discord_user 
            WHERE discord_id = %s
        """, (discord_id,))

        result = self.cur.fetchone()
        if result is None:
            self.if_new(interaction)

            new_played_games = 1
            current_lose = 0

        else:
            current_lose = result[0] if result and result[0] is not None else 0
            cur_played_games = result[1] if result and result[1] is not None else 0

            new_played_games = cur_played_games + 1
        new_lose = current_lose + gold

        self.cur.execute("""
            UPDATE discord_user
            SET lost = %s, played_games = %s
            WHERE discord_id = %s
        """, (new_lose,new_played_games, discord_id))
        
        self.conn.commit()

    def show_user(self, interaction: discord.Interaction):
        discord_id = interaction.user.id
        self.cur.execute("""
        SELECT won, lost, played_games
        FROM discord_user 
        WHERE discord_id = %s
        """, (discord_id,))

        return self.cur.fetchone()
    
    def shut_down(self):
        self.cur.close()
        self.conn.close()


    def __str__(self):
        self.cur.execute("""
        SELECT name, won, lost, played_games
        FROM discord_user 
        ORDER BY (won-lost) DESC
        LIMIT 10
        """)

        output = "```"
        output += "Name          | Score    | Played\n"
        output += "-" * 33 + "\n"

        for x in self.cur.fetchall():
            name = str(x[0])[:13]  
            score = x[1] - x[2]

            if score >= 0:
                colour = "🟩"
            else:
                colour = "🟥"
                score *= -1

            played = x[3]
            output += f"{name.ljust(13)} | {colour}{str(score).ljust(6)} | {str(played).ljust(6)}\n"

        output += "```"
                
        return output
    
    




class BlackEmbed(discord.ui.View):
    suit_emojis = {
        '♤': '♠️',
        '♡': '♥️',
        '♢': '♦️',
        '♧': '♣️',
    }

    def __init__(self, game: BlackJack, username: str,user_data, interaction: discord.Interaction):
        super().__init__(timeout=300)
        self.game = game
        self.username = username
        self.finished = False
        self.message = None
        self.user_data = user_data
        self.interaction = interaction
        self.author = interaction.user.id 

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

            if box == "🟩":
                self.user_data.win_gold(self.game.bet_amount, self.interaction)
            elif box == "🟥":
                self.user_data.lose_gold(self.game.bet_amount, self.interaction)


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
            if self.author == interaction.user.id:
                user_id = interaction.user.id
                new_game = BlackJack()

                if self.game.been_doubled:
                    self.game.back_from_double()
                    
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


                new_view = BlackEmbed(new_game, username,self.user_data, interaction)
                embed = new_view.display_hands()
                sent = await interaction.followup.send(embed=embed, view=new_view)
                new_view.message = sent
            else:
                await interaction.followup.send("wrong player miko things")

        button.callback = callback
        return button

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.blurple, emoji="🃏")
    async def hit_button(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.defer()

        if self.author == interaction.user.id:
            self.game.hit()
            if self.game.calculate_total(self.game.user_hand) > 21:
                await self.end_game(interaction)
            else:
                await interaction.message.edit(embed=self.display_hands(), view=self)
        else:
            await interaction.followup.send("wrong player miko things")

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.blurple, emoji="🖐️")
    async def stand_button(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if self.author == interaction.user.id:
            self.game.stand()
            await self.end_game(interaction)
        else:
            await interaction.followup.send("wrong player miko things")

    @discord.ui.button(label="Double Down", style=discord.ButtonStyle.green, emoji="🤑")
    async def double_button(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if self.author == interaction.user.id:
            self.game.double()
            self.game.stand()
            await self.end_game(interaction)
        else:
            await interaction.followup.send("wrong player miko things")


class GambleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}
        self.roulette = Roulette()
        self.user_data = SqlData()
        


    @app_commands.command(name="blackjack", description="Play a round of Blackjack with Miko!")
    async def blackjack_command(self, interaction: Interaction, printer: int):
        await interaction.response.defer()
        try:
            user_id = interaction.user.id
            if user_id in self.active_games:
                del self.active_games[user_id]

            game = BlackJack()
            game.new_game(printer)
            self.active_games[user_id] = game

            view = BlackEmbed(game, interaction.user.display_name, self.user_data, interaction)
            embed = view.display_hands()
            await interaction.followup.send(embed=embed, view=view)

            view.message = await interaction.original_response()
        except ValueError as problem:
             await interaction.followup.send(problem)


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
                self.user_data.win_gold(gold, interaction)
            else:
                add_on = f"Miko is sad for you... \n\n\u2003🟥 {gold}"
                self.user_data.lose_gold(gold, interaction)
        

            embed = discord.Embed(title="🪙Roulette", description="**Miko is not responsible for your gambling addiction!!**", color=0x7851A9)
            embed.set_image(url=gif)
            embed.add_field(name=message, value=add_on, inline=False)
            embed.add_field(name="Your bet:", value=printer, inline=True)
            embed.add_field(name="Result:", value=result, inline=True)
            embed.add_field(name="Colour:", value=colour, inline=True)
            embed.set_footer(text="finding gif that would work better is appreaticated")
            await interaction.response.send_message(embed=embed)
        self.bot.miko_used()


    @app_commands.command(name="look_see", description="Do you want Miko to give you pure gambling stats")
    async def look_see_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="✨Roulette Stats✨",
            color=0x008000,
            description= f"**Miko's love for numbers**\n\n")
        embed.description += str(self.roulette)
        await interaction.response.send_message(embed=embed)
        self.bot.miko_used()


    @app_commands.command(name="ranks", description="who is just that good at gambling")
    async def rank_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="✨RANKS✨",
            color=0x008000,
            description= f"**Miko feel like most of ya are in the negative**\n\n")
        embed.description += str(self.user_data)
        await interaction.response.send_message(embed=embed)
        self.bot.miko_used()


    @app_commands.command(name="my_self", description="sometime stats could make you stop")
    async def my_self_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="✨YOUR PROFITS✨",
            color=0x008000,
            description= f"**Miko knows you got this**\n\n")
        
        user = self.user_data.show_user(interaction)
        total = user[0] - user[1]
        embed.add_field(name="Your Total:", value=total, inline=True)
        embed.add_field(name="Your total won:", value=f"🟩{user[0]}", inline=True)
        embed.add_field(name="Your total lose:", value=f"🟥{user[1]}", inline=True)
        embed.add_field(name="Your total games played:", value=user[2], inline=False)
        await interaction.response.send_message(embed=embed)
        self.bot.miko_used()


    #i know i have a shut down but unless i move sqldata into another file this is the best
    #but i am lazy will do later maybe

    @app_commands.command(name="shutdown2", description="i know i know i am bad")
    async def shutdown2_command(self, interaction: discord.Interaction):
        await interaction.response.send_message("Shutdown sql")
        self.user_data.shut_down()


async def setup(bot):
    await bot.add_cog(GambleCog(bot))