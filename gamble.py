import random
import json
import os


class Roulette():

    #still trying to find all the gifs for the roulette wheel
    _roulette = {
    0: {"colour": "green", "gif": "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZTFicDhzYWhhZ3F6cGx6Zmh1eXIycXZlMWh6M3VxdmtlNmFyY2U3ZiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/PnZuQqvuzYayiXe0mx/giphy.webp"}, #x
    1: {"colour": "red", "gif": "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExbTYzaDJwYjY4cWk5c3Nyb3pueGNwczg0OTY4NWRtYnVrdHIzb3U2MyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/xT1XGAp9fzhlPXKJQk/giphy.webp"}, #✅
    2: {"colour": "black", "gif": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExbjRlbjhjZ3NubjAxOXN5bjUzaHZuMWxnNmkwNzQ5OWk1eTY0Y2JpaSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/cNYPlsYn4DoYzHgoca/giphy.webp"}, #❌
    3: {"colour": "red", "gif": "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExZzJqcmh1OG5qMjdwbm5mNGNmamZzbnZ0bDN6bXJiZHR0ZGx1OG5vMSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Y0VFEdJxkE2H0qSoA8/giphy.webp"}, #❌
    4: {"colour": "black", "gif": "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExZjBsc255MjJsMnQ5eWwycHdpNWQ1NDJ3cWIxbnVhc3ZqZjBvMzJhbiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/9fnTf6pMNP5Rx78rTG/giphy.webp"}, #❌
    5: {"colour": "red", "gif": "https://media3.giphy.com/media/KAj2vV0L8OOQ7yJdtU/giphy.webp?cid=ecf05e475s8mflhxt0mpqkowtu2w3u7mtli9m8d4mck0t1ge&ep=v1_gifs_search&rid=giphy.webp&ct=g"}, #✅
    6: {"colour": "black", "gif": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExbG0yOXZ6eTA4Y2hhM291dHF2Zngza3N3YjZudzJtMzd0YjhnejE5ZSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/PbMLgugTPJnwE0Fnn2/giphy.webp"}, #✅
    7: {"colour": "red", "gif": "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExcnYxdzlqenkwdHMyY2VwZGp1ejF3djl2bmN6bnRjaGcwY3Y1cnkxYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3orifaWiKhGkPGg1Ow/giphy.gif"}, #✅
    8: {"colour": "black", "gif": "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmUyMW55M2RhdXR5cHNzOTljeXk5Z2xveHd3bTR3aDhiMDB4czQ3OSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/H4zxFJSaCQtxtFsoXe/200.webp"}, #✅
    9: {"colour": "red", "gif": "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExZXYwMzg5b2Z0ZmVsb2hyMzNlaHd0bG9iYnJieDRoM3dvYTdkeHpiciZlcD12MV9naWZzX3NlYXJjaCZjdD1n/vtHfKoGsOec3sHi61H/200.webp"}, #✅
    10: {"colour": "black", "gif": "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExMzhwY3ViOGVyc3VwdDhheHNoZDEwZ2htbjNjcnhhamp0Y3Rqc2VzbSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/iFnBpFxFGetn8BH0vZ/200.webp"}, #❌
    11: {"colour": "black", "gif": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExa3l2ZnVjcHBjbW93MW5iZWM3dmNrb2xub2luYnl3bzQ3Zno0bGc0NSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/5Szs80FJTKDHQmA1SD/200.webp"}, #❌❌
    12: {"colour": "red", "gif": "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExOTZmbDZ4eG9wMDNoaDlnOXJqeWQzMW8xZGt6NzJmajFnNGV6d2NhciZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Ng1ZRRz3QRy5BhTNST/200.webp"}, #❌
    13: {"colour": "black", "gif": "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExOXZ4MTBza3VtZm9hdjcyaGN0dzc4ZXpqandrdTRhbHc3czZodHRyOCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/o9VujcY3Iv2ve/giphy.webp"}, #❌
    14: {"colour": "red", "gif": "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExbW83dXN6azlpbDE4cXZ5eGgxNnRwYXI1MTByZWo1d29vaDE5MnAxMyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/jtQ8XoCJe92qxUdZRR/giphy.webp"}, #❌
    15: {"colour": "black", "gif": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ3psdDFidzNod2Rrd3FhOTc3NzM1Y21xcXpkNXYzMmsxa3B2NG84YSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/qKgWBHKKbmAwk9n9Wr/giphy.webp"}, #❌
    16: {"colour": "red", "gif": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDhidnRqdGYzN2ZhZWYwZnlxZ29uZTFqcDVwZDdsdGdndzN6cHJuMyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/4U4hy63YFqpmgN90mg/giphy.webp"}, #❌❌
    17: {"colour": "black", "gif": "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3gydWxwMmtxenNhNmU1cjlqaDEydnRoMjByZ2NlYWxiODNtOXkxbyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/3oz8xMsEVYySEOVcVG/giphy.webp"}, #❌❌
    18: {"colour": "red", "gif": "https://media4.giphy.com/media/hmxzrWrQrHKdYBZeZW/200.webp?cid=ecf05e476uqwstbhsz0idvrsvrbmsvgm4qtp1a3feqh9bsy8&ep=v1_gifs_search&rid=200.webp&ct=g"}, #❌❌
    19: {"colour": "red", "gif": "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExODFuNGRjbmRkNWxvNGM1MXFmaWo1N2ozdWV6ZHdlandsazBuajczOCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/e6gldzwauUfb56NWap/giphy.webp"}, #❌
    20: {"colour": "black", "gif": "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExY2dtODBtZDAydjl5cDJxdDV3bGplZHhvYm9pcDRudzd4b3dwZXhhbCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/MXdXSV2wCyv5kwXmSH/giphy.webp"}, #❌
    21: {"colour": "red", "gif": "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExeDhiaTJlZHI1MXY4N3U3NTl2dW5qd2E3Z2kzb3plazkxdGZvb2tyNyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/E5j9VLw6goskDbjd3U/giphy.webp"}, #❌❌
    22: {"colour": "black", "gif": "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ2xjZHhsbHRnNHFybWU1Y3lyNXBwZjAzNjA4YjQyN3dtZTh1NmdoeiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/K6VimBsJbfLPeqVyqS/giphy.webp"}, #❌
    23: {"colour": "red", "gif": "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExbHJ4Y3Z3NzNsdmhvMXg1Y25jdXFtdG51dWpiaW9qOXJ1YzhiczFmciZlcD12MV9naWZzX3NlYXJjaCZjdD1n/1zKRm7xZjkhaeeZbSd/giphy.webp"}, #❌
    24: {"colour": "black", "gif": "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExNzZ4eWg4YWo0bHd5bzhnc3A0c29pNDUyNDRqNTJrOGhtdTg4aGpuZyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/WrUaNTONeaKaLsPi0O/giphy.webp"}, #❌
    25: {"colour": "red", "gif": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExamppZW0weHdyb2o2bnA1YTN1b2F6MjVqNWd1Z2liM2JuZWg2eDE4YSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/xhKRY1FFpoC2GmzDAr/giphy.webp"}, #❌❌
    26: {"colour": "black", "gif": "https://media4.giphy.com/media/LapzctxH4QoVx5X0wv/giphy.webp?cid=ecf05e47acgl5te7h8ozlspt58kdwb2tso3esdy9g7p3ohv1&ep=v1_gifs_search&rid=giphy.webp&ct=g"}, #❌❌
    27: {"colour": "red", "gif": "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExb213Nmg1OTE4Mnk1cXdwdjVybnpncjFhcjJwcDc3aXY5bmF2cmpwbiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/26gJALIRlvPcw9sxq/giphy.webp"}, #❌
    28: {"colour": "black", "gif": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNnEzeWd5ZmF1ankzZDg4M2Z3MHJodjJvanExajYzZnRhcXF5ZHJxZCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/5xtDarsM8jmOJtlOeTm/200.webp"}, #❌❌
    29: {"colour": "black", "gif": "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdnh4aWt1dDRrdjM2bDF6NDRkamphenRnYXFvNjUzZG5vcTlmdjZmMiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/l0HlRPGDG8PPfdH1K/giphy.webp"}, #❌❌
    30: {"colour": "red", "gif": "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExc3o4M2JqNzZ2OXdsNDZkam5xZjRtNGZwMWYwcTA4M21oMzI3anJnbyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/xUA7b7O3atoEknirKg/giphy.webp"}, #❌❌
    31: {"colour": "black", "gif": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExODRhbDh6bTc4enp6b3B6eGFqaGQ4b2FlNDBoaHBhMjlkZXc3YTVxZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26uflBhaGt5lQsaCA/giphy.gif"}, #✅
    32: {"colour": "red", "gif": "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExNDR3MHVrbnQ0OTNpaGE3MmVyODFheG9jcGUxaG50MmJqeHdwamdobiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Y2afFWuk70aDHCek66/200.webp"}, #❌
    33: {"colour": "black", "gif": "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExa3JzMDJhd3M3Mno4OHgzMXd5Z29ldWFzeWQ0ODN5dmplZmlzZ21xdiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/iKJky4zNd6E7TEs5Le/200.webp"}, #❌
    34: {"colour": "red", "gif": "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExMnM0NmFuMDZ3aGltNGZmYm9zYnQzdWRhMm96YzBjbXd3aGFpdzRvMyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/x1IKfP2igMWGElYvx3/giphy.webp"}, #❌❌
    35: {"colour": "black", "gif": "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExZGRybTZiYjd6cm95cXllcHF2NXUydnBoaGtybjhhem95Zm1uZ3liOCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/q1ol7pCEdr9WgVHH68/giphy.webp"}, #❌❌
    36: {"colour": "red", "gif": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExYmduZmVlZXQ1NGQ0NW9yODJ3endpeXJobTNvenV2cDA5d3p2czdldyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/719pIPPBuXD3Id0fQM/giphy.webp"} #❌❌
}
    
    possible_bets = {
        "red": 2,
        "black": 2,
        "low": 2,
        "high": 2,
        "even": 2,
        "odd": 2,
        "1st12": 3,
        "2nd12": 3,
        "3rd12": 3
    }

    def __init__(self, data_file="roulette_table.json"):
        self.data_file = data_file
        self.miko_data = self.load_roulette_data()

        self.wins = self.miko_data["wins"]
        self.total_bets = self.miko_data["total_bets"]
        self.result_numbers = self.miko_data["result_numbers"]

    
    def load_roulette_data(self):
        if not os.path.exists(self.data_file):
            return {
                "wins" : {
                    "red": 0,
                    "black": 0,
                    "green": 0
                },
                "total_bets" : 0,
                "result_numbers": {
                    "0": 0,
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0,
                    "10": 0,
                    "11": 0,
                    "12": 0,
                    "13": 0,
                    "14": 0,
                    "15": 0,
                    "16": 0,
                    "17": 0,
                    "18": 0,
                    "19": 0,
                    "20": 0,
                    "21": 0,
                    "22": 0,
                    "23": 0,
                    "24": 0,
                    "25": 0,
                    "26": 0,
                    "27": 0,
                    "28": 0,
                    "29": 0,
                    "30": 0,
                    "31": 0,
                    "32": 0,
                    "33": 0,
                    "34": 0,
                    "35": 0,
                    "36": 0
                }
            }
        with open(self.data_file, "r") as f:
            return json.load(f)

    def save_Roulette_data(self, data):
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=4)


    def spin(self):
        result = random.randint(0, 36)
        colour = self._roulette[result]["colour"]

        gif = self._roulette[result]["gif"]

        # Update the data
        self.total_bets += 1
        self.wins[colour] += 1
        self.result_numbers[str(result)] += 1
        self.miko_data["result_numbers"] = self.result_numbers
        self.miko_data["wins"] = self.wins
        self.miko_data["total_bets"] = self.total_bets
        self.save_Roulette_data(self.miko_data)

        return result, colour, gif

    def get_bet(self, bet):
        #bet is split from gold.bet_type
        bet = bet.split(".")
        if len(bet) == 2:
            gold = int(bet[0])
            bet_type = bet[1]
            return gold, bet_type
        else:
            return None, None
        
    def roulette_bet(self, bet):
        try:    
            gold, bet_type = self.get_bet(bet)
        except ValueError:
            return "Miko spins in confusion! That’s not real gold! Check the rules, silly!", None, None

        if gold is None or bet_type is None:
            return "Miko chirps: Format wrong! Try it like this — '100.red' or '50.17'!", None, None

        elif gold <= 0 or gold > 500:
            return "Miko raises an eyebrow. That gold amount is suspicious... Keep it between 1 and 500!", None, None

        elif (bet_type not in self.possible_bets and not bet_type.isdigit() and '_' not in bet_type):
            return "Miko spins in confusion! That’s not a real bet type! Check the rules, silly!", None, None
        


        #get the result of the spin
        result, colour, gif = self.spin()
        win = False
        multiplier = 0

        # Split number bets:  300.5_8_11
        if '_' in bet_type:
            split_bet = bet_type.split('_')
            if all(num.isdigit() and 0 <= int(num) <= 36 for num in split_bet):
                if str(result) in split_bet:
                    win = True
                    multiplier = 36 // len(split_bet)
            else:
                return "Miko tilts his head... one of those numbers isn’t real! Use 0–36 only.", None, None, None, None

        elif bet_type.isdigit():
            if not (0 <= int(bet_type) <= 36):
                return "Miko flaps in panic! That number isn’t on the wheel! 🎲", None, None, None, None
            if int(bet_type) == result:
                win = True
                multiplier = 36

        else:
            if bet_type == colour:
                win = True
                multiplier = self.possible_bets[colour]
            elif bet_type == "low" and result <= 18:
                win = True
                multiplier = self.possible_bets["low"]
            elif bet_type == "high" and result > 18:
                win = True
                multiplier = self.possible_bets["high"]
            elif bet_type == "even" and result % 2 == 0 and result != 0:
                win = True
                multiplier = self.possible_bets["even"]
            elif bet_type == "odd" and result % 2 == 1:
                win = True
                multiplier = self.possible_bets["odd"]
            elif bet_type == "1st_12" and 1 <= result <= 12:
                win = True
                multiplier = self.possible_bets["1st_12"]
            elif bet_type == "2nd_12" and 13 <= result <= 24:
                win = True
                multiplier = self.possible_bets["2nd_12"]
            elif bet_type == "3rd_12" and 25 <= result <= 36:
                win = True
                multiplier = self.possible_bets["3rd_12"]

        if win:
            winnings = gold * multiplier
            return f"Miko squeaks happily! You won {winnings} gold! 🎉", gif, True, colour, result, winnings
        else:
            return f"Miko gasps... no win this time. You lost {gold} gold. 😢", gif, False, colour, result, gold

    def top_wins(self):
        max_result = max(self.result_numbers, key=lambda x: self.result_numbers[x])
        return f"Miko has been watching... and the wheel loves the number {max_result},\n\
it showed up {self.result_numbers[max_result]} times!🎲👀"
    
    def __str__(self):
        output = []
        output.append("🎯 **Roulette Data**\n")
        output.append("**Wins:**\n")

        # Use emoji bullets and aligned values
        for color in ["red", "black", "green"]:
            count = self.wins.get(color, 0)
            emoji = {"red": "🔴", "black": "⚫", "green": "🟢"}[color]
            output.append(f"> {emoji} **{color.capitalize():<6}**: {count}\n")

        output.append(f"\n🎲 **Total Bets:** `{self.total_bets}`\n\n")

        # Add the top wins section
        output += self.top_wins()  # assumes this returns a list of strings or formatted text

        return "".join(output)
    
def test_class():
    roulette = Roulette()
    print(roulette.roulette_bet("100.red"))
    print(roulette.roulette_bet("100.black"))
    print(roulette.roulette_bet("100.1st12"))
    print(roulette.roulette_bet("100.2nd12"))
    print(roulette.roulette_bet("100.3rd12"))
    print(roulette.roulette_bet("100.even"))
    print(roulette.roulette_bet("100.odd"))
    print(roulette.roulette_bet("100.low"))
    print(roulette.roulette_bet("100.high"))
    print(roulette.roulette_bet("100.0"))
    print(roulette.roulette_bet("100.6"))
    print(roulette.roulette_bet("100.5"))
    print(roulette.roulette_bet("100.12"))
    print(roulette.roulette_bet("100.18_12"))
    print(roulette.roulette_bet("100.0_1_2_3_4_5_6_7_8_9_10_11_12"))
    print(roulette)

if __name__ == "__main__":
    test_class()