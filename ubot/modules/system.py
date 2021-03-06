# SPDX-License-Identifier: GPL-2.0-or-later

import asyncio
from platform import python_version, uname
from time import time_ns

from telethon import version

from ubot.micro_bot import micro_bot

ldr = micro_bot.loader


@ldr.add("reload")
async def reload_modules(event):
    await event.edit("`Reloading modules…`")

    errors = ldr.reload_all_modules()

    if errors:
        await event.edit(errors)
    else:
        try:
            await event.delete()
        except:
            pass


@ldr.add("help")
async def help_cmd(event):
    help_string = ""

    for key, value in ldr.help_dict.items():
        help_string += f"\n**{key}**: "
        for info in value:
            help_string += f"`{info}`, "
        help_string = help_string.rstrip(", ")

    await event.edit(f"`Available commands:`\n{help_string}")


@ldr.add("sysd")
async def sysd(event):
    try:
        neo = "neofetch --stdout"

        fetch = await asyncio.create_subprocess_shell(
            neo,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await fetch.communicate()

        await event.edit(f"`{stdout.decode().strip()}{stderr.decode().strip()}`")
    except FileNotFoundError:
        await event.edit("`Neofetch not found!`")


@ldr.add("alive")
async def alive(event):
    alive_format = "`μBot is running under {0}.\n\n" \
                   "Version: {1}\n" \
                   "Telethon: {2}\n" \
                   "Python: {3}`"

    await event.edit(alive_format.format(uname().node, ldr.botversion, version.__version__, python_version()))


@ldr.add("shutdown")
async def shutdown(event):
    await event.edit("`Goodbye…`")
    await micro_bot.stop_client()


@ldr.add("ping")
async def ping(event):
    start = time_ns()
    await event.edit("`Ping…`")
    time_taken_ms = int((time_ns() - start) / 1000000)
    await event.edit(f"`Ping… Pong! -> `**{time_taken_ms}**`ms`")


@ldr.add("prefix")
async def change_prefix(event):
    new_prefix = event.args

    if not new_prefix:
        await event.edit("`Please specify a valid command prefix!`")
        return

    micro_bot.settings.set_config("cmd_prefix", new_prefix)

    await event.edit(f"`Command prefix successfully changed to `**{new_prefix}**`!`")


@ldr.add("repo")
async def bot_repo(event):
    await event.edit("https://github.com/Nick80835/microbot")


@ldr.add("toggleincoming")
async def toggleincoming(event):
    if micro_bot.settings.get_bool("incoming_allowed"):
        micro_bot.settings.set_config("incoming_allowed", "False")
        await event.edit("`Successfully disabled incoming commands!`")
    else:
        micro_bot.settings.set_config("incoming_allowed", "True")
        await event.edit("`Successfully enabled incoming commands!`")
