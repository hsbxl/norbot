import random
import requests

from matrix_bot_api.matrix_bot_api import MatrixBotAPI
from matrix_bot_api.mregex_handler import MRegexHandler
from matrix_bot_api.mcommand_handler import MCommandHandler

USERNAME = "norbert"  # Bot's username
PASSWORD = ""  # Bot's password
SERVER = "https://hackerspace.be"  # Matrix server URL


def troll_callback(room, event):
    args = event['content']['body'].split()
    args.pop(0)
    sentence = "SPEAK="+" ".join(args)

    url = "http://hal9000.space.hackerspace.be/cgi-bin/sounds.sh"
    r = requests.post(url, data=sentence)
    room.send_text("🎶 They see me Trolling 🎶")

def hours_callback(room, event):
    message = "We have our weekly TechTuesday every Tuesday evening. This night the space is open for everyone, members and visitors."
    room.send_text(message)

def hi_callback(room, event):
    # Somebody said hi, let's say Hi back
    room.send_text("Hi, " + event['sender'])


def dieroll_callback(room, event):
    # someone wants a random number
    args = event['content']['body'].split()

    # we only care about the first arg, which has the die
    die = args[0]
    die_max = die[2:]

    # ensure the die is a positive integer
    if not die_max.isdigit():
        room.send_text('{} is not a positive number!'.format(die_max))
        return

    # and ensure it's a reasonable size, to prevent bot abuse
    die_max = int(die_max)
    if die_max <= 1 or die_max >= 1000:
        room.send_text('dice must be between 1 and 1000!')
        return

    # finally, send the result back
    result = random.randrange(1,die_max+1)
    room.send_text(str(result))



def main():
    # Create an instance of the MatrixBotAPI
    bot = MatrixBotAPI(USERNAME, PASSWORD, SERVER)

    # Add a regex handler waiting for the word Hi
    hi_handler = MRegexHandler("Hi", hi_callback)
    bot.add_handler(hi_handler)

    # Add a regex handler waiting for the die roll command
    dieroll_handler = MCommandHandler("d", dieroll_callback)
    bot.add_handler(dieroll_handler)

    # Add a regex handler waiting for the troll command
    troll_handler = MCommandHandler("troll", troll_callback)
    bot.add_handler(troll_handler)

    # Add a regex handler waiting for the hours command
    hours_handler = MCommandHandler("hours", hours_callback)
    bot.add_handler(hours_handler)

    # Start polling
    bot.start_polling()

    print(bot)

    # Infinitely read stdin to stall main thread while the bot runs in other threads
    while True:
        input()



if __name__ == "__main__":
    main()