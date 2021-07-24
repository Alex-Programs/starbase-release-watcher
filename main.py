import asyncio
from discord import client, Intents
from discord.ext import commands

import datetime

import store


def log(text):
    with open("logs.txt", "a") as f:
        f.write(text + "\n")

    print(text)


class persistent():
    released = False


ownerID = 318756837266554881


def owner():
    def predicate(ctx):
        if ctx.author.id == ownerID:
            return True

        return False

    return commands.check(predicate)


RELEASE_MESSAGE = """
Starbase Early Access has released on Steam! https://store.steampowered.com/app/454120/Starbase/

After years of waiting, the day is finally here."""

intents = Intents.default()
intents.members = True

client = commands.Bot(command_prefix="=", intents=intents)

def getTime():
    present = datetime.datetime.now()
    release = datetime.datetime.fromtimestamp(1627570800)

    left = release - present

    count_hours, rem = divmod(left.seconds, 3600)
    count_minutes, count_seconds = divmod(rem, 60)

    return f"{left.days}d {count_hours}h {count_minutes}m {count_seconds}s"


async def update_release_status():
    while True:
        await asyncio.sleep(5)
        try:
            released = store.is_released("454120")
        except:
            log("Something went wrong with the check")
            released = False
            pass

        if released:
            log("RT")
        else:
            log("RF")

        if released and not persistent.released:
            await send_dms()
            with open("released.txt", "w") as f:
                f.write("1")

        persistent.released = released


async def send_dms():
    with open("notifyUsers.txt") as f:
        log("Conducting mass DM due to SB release.")
        for user in f.readlines():
            await asyncio.sleep(0.2)
            await client.get_user(int(user)).send(RELEASE_MESSAGE)


@client.event
async def on_ready():
    client.loop.create_task(update_release_status())
    log(f"Logged on as {client.user}")


@client.command()
async def outyet(ctx):
    log("Outyet queried by " + str(ctx.author.id) + " aka " + ctx.author.name)
    if persistent.released:
        return await ctx.send("""**Starbase Early Access has Released!**
        
https://imgur.com/GQMacSz""")
    else:
        timeLeft = getTime()

        return await ctx.send(f"""**Starbase Early Access isn't released yet.**
        
But it's almost there. Just ```diff
- {timeLeft} -
``` to go!*

Please don't spam this command! Go to https://countdown.centralmind.net instead.

*time is approximate. However, release status is not.""")


@client.command()
async def notifyme(ctx):
    with open("notifyUsers.txt") as f:
        if str(ctx.author.id) in f.read():
            return await ctx.send("You've already been added!")

    with open("notifyUsers.txt", "a") as f:
        f.write(str(ctx.author.id) + "\n")

    log(f"Added {str(ctx.author.id)} aka {ctx.author.name} to notify list.")
    return await ctx.send("You have been added to the list of users to notify when Starbase releases.")

@owner()
@client.command()
async def manual_alert(ctx):
    await ctx.send("Sending manual alert")
    await send_dms()
    await ctx.send("Done")

with open("token.txt") as f:
    token = f.read()

with open("released.txt") as f:
    if f.read() == "0":
        persistent.released = False
    else:
        persistent.released = True

client.run(token)
