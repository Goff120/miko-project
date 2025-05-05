import random
import json
import os


class Gamble():

    _roulette = {
    0: {"colour": "green", "gif": "https://tenor.com/tgzdfDbAwvw.gif"},
    1: {"colour": "red", "gif": "https://tenor.com/rggieMGC3ie.gif"},
    2: {"colour": "black", "gif": "url2"},
    3: {"colour": "red", "gif": "url3"},
    4: {"colour": "black", "gif": "url4"},
    5: {"colour": "red", "gif": "https://tenor.com/qnSj8Pk2Sui.gif"},
    6: {"colour": "black", "gif": "https://tenor.com/eZp3K1DT2Hw.gif"},
    7: {"colour": "red", "gif": "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExcnYxdzlqenkwdHMyY2VwZGp1ejF3djl2bmN6bnRjaGcwY3Y1cnkxYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3orifaWiKhGkPGg1Ow/giphy.gif"},
    8: {"colour": "black", "gif": "https://tenor.com/bp7foFcOjvD.gif"},
    9: {"colour": "red", "gif": "https://tenor.com/beyFU.gif"},
    10: {"colour": "black", "gif": "url10"},
    11: {"colour": "black", "gif": "url11"},
    12: {"colour": "red", "gif": "url12"},
    13: {"colour": "black", "gif": "url13"},
    14: {"colour": "red", "gif": "url14"},
    15: {"colour": "black", "gif": "url15"},
    16: {"colour": "red", "gif": "url16"},
    17: {"colour": "black", "gif": "url17"},
    18: {"colour": "red", "gif": "url18"},
    19: {"colour": "red", "gif": "url19"},
    20: {"colour": "black", "gif": "url20"},
    21: {"colour": "red", "gif": "url21"},
    22: {"colour": "black", "gif": "url22"},
    23: {"colour": "red", "gif": "url23"},
    24: {"colour": "black", "gif": "url24"},
    25: {"colour": "red", "gif": "url25"},
    26: {"colour": "black", "gif": "url26"},
    27: {"colour": "red", "gif": "url27"},
    28: {"colour": "black", "gif": "url28"},
    29: {"colour": "black", "gif": "url29"},
    30: {"colour": "red", "gif": "url30"},
    31: {"colour": "black", "gif": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExODRhbDh6bTc4enp6b3B6eGFqaGQ4b2FlNDBoaHBhMjlkZXc3YTVxZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26uflBhaGt5lQsaCA/giphy.gif"},
    32: {"colour": "red", "gif": "url32"},
    33: {"colour": "black", "gif": "url33"},
    34: {"colour": "red", "gif": "url34"},
    35: {"colour": "black", "gif": "url35"},
    36: {"colour": "red", "gif": "url36"}
}
    
    possible_bets = {
        "red": 2,
        "black": 2,
        "low": 2,
        "high": 2,
        "even": 2,
        "odd": 2,
        "1st_12": 3,
        "2nd_12": 3,
        "3rd_12": 3
        
    }

    def __init__(self, data_file="roulette_table.json"):
        self.data_file = data_file
        self.miko_data = self.load_roulette_data()

        self.wins = self.miko_data["wins"]
        self.total_bets = self.miko_data["total_bets"]

    
    def load_roulette_data(self):
        if not os.path.exists(self.data_file):
            return {
                "wins" : {
                    "red": 0,
                    "black": 0,
                    "green": 0
                },
                "total_bets" : 0
                }
        with open(self.data_file, "r") as f:
            return json.load(f)

    def save_Roulette_data(self, data):
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=4)


    def spin(self):
        result = random.randint(0, 37)
        colour = self._roulette[result]["colour"]

        gif = self._roulette[result]["gif"]

        # Update the data
        self.total_bets[colour] += 1
        self.wins[colour ] += 1
        self.miko_data["wins"] = self.wins
        self.miko_data["total_bets"] = self.total_bets
        self.save_Roulette_data(self.miko_data)

        return result, colour, gif

    def get_bet(self, bet):
        #bet is split into gold.bet_type
        bet = bet.split(".")
        if len(bet) == 2:
            gold = bet[0]
            bet_type = bet[1]
            return gold, bet_type
        else:
            return None, None
        
    def roulette_bet(self, bet):
        gold, bet_type = self.get_bet(bet)

        if gold is None or bet_type is None:
            return "Invalid bet format. Please use 'gold.bet_type' format."
        
        elif gold <= 0 or gold > 500:
            return "Invalid gold amount. Please enter a value between 1 and 500."
        
        elif (bet_type not in self.possible_bets and not bet_type.isdigit()):
            return "Invalid bet type. Please choose from the rules"
        
        elif bet_type.isdigit() and not (0 <= int(bet_type) <= 36):
            return "Miko flaps in panic! That number isn’t on the wheel! 🎲"
        
        else:
            result, colour, gif = self.spin()
            win = False
            multiplier = 0

            # Check bet match and set win state
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
            elif bet_type.isdigit() and int(bet_type) == result:
                win = True
                multiplier = 36

            # Final return
            if win:
                return f"Congratulations! You won {gold * multiplier} gold! 🎉", gif
            else:
                return f"Sorry, you lost {gold} gold. Better luck next time! 😢", gif

        


    def __str__(self):
        output = []
        output += ['Roulette Data:\n']
        output += [f'wins: \n']
        for color, count in self.wins.items():
            output += [f'   -{color}: {count}\n']

        output += [f'losses: \n']
        for color, count in self.losses.items():
            output += [f'   -{color}: {count}\n']

        output += [f'total_bets: \n']
        for color, count in self.total_bets.items():
            output += [f'   -{color}: {count}\n']

        return "".join(output)
    


roulette = Gamble()
print(roulette)