from itertools import count
import json
import usb.core
from escpos.printer import Usb
from discord import *
import textwrap

with open('config.json', 'r') as f:
    config = json.load(f)

key = config['key']
loc = config['location'].split(':')
p = Usb(loc[0], loc[1], 0, profile=config['profile'])
client = Client(intents=Intents.all())

async def reline(content):
    back = ""
    set = []

    con = content.split("\n")
    for element in con:
        if len(element) > config["width"]:
            set.append(textwrap.fill(element, width=config["width"]))
        else:
            set.append(element)

    for element in set:
        back = f"{back}\n{element}"

    return back

async def printout(message):
    try:
        p.set(align="center", bold=True, double_height=True, double_width=True)
        p.text(message.author.display_name)
        p.set(double_height=False, double_width=False, normal_textsize=True)
        p.text(f"\n{message.author.name}\n{message.author.id}")
        p.set(bold=False)
        p.text(f"\n{message.created_at}")
        p.ln(count=2)
        p.set(align="left")
        if len(message.attachments) == 1:
            if message.attachments[0].filename == "message.txt":
                longcontents = await message.attachments[0].read(use_cached=False)
                longcontents = longcontents.decode()
                p.text(await reline(longcontents))
        else:
            p.text(await reline(message.content))
        p.ln(count=2)
        p.cut()
    except usb.core.USBError:
        await message.reply("Printer not responding, for some reason.")

@client.event
async def on_message(message):
    if not message.guild:
        if message.content == "!cut":
            p.cut()
        else:
            await printout(message)

@client.event
async def on_ready():
    print('-----')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')

client.run(str(key))
