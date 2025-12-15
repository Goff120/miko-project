from random import choice

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

        
            "Roulette":
            "using the `/roulette` command.\n"\
            "Place bets using the format gold.bet_type.\n"\
            "Available types include: \nred, black, even, odd, low, high, 1st12, 2nd12,3rd12\n"\
            "You can also bet on single or multiple numbers.\n"\
            "For multiple numbers, use a format like 400.13_18.\n"\
            "To see what's currently popular on the table, use `/look_see`.\n\n"\
            "Note: The GIFs are currently not working well.\n"\
            "Miko uses the Eurpean wheel so no 00",

            "Blackjack":
            "`/blackjack` command just needs the input of the gold you want to put in\n"\
            "at the start you can see mikos first card and both yours\n"\
            "hit and draw a new card\n"\
            "stand and miko will take over\n"\
            "double draws a card doubles your bet past that can pass 500 and ends your drawing\n"\
            "miko will stop drawing cards when he at leasts gets to 17",

            "Gambling":
            "`/ranks` lets you see the top 10 best gamblers (not the loser)\n"\
            "`/my_self` you can see how much you lose and win and games played\n"\
            "finally we can see how mcuh of a loser you are",

            
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