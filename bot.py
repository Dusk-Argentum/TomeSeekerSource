"""
Written by @zhu.exe#4211 (187421759484592128).
"""
import asyncio
import os

import aiohttp
from discord.ext import commands
from discord.ext.commands import CommandInvokeError

from funcs import *

OWNER_ID = "97153790897045504"

PREFIX = "." # This is the prefix you call commands with in Discord. For example: ".help" will call the the "Help" command, but only if your prefix is ".".
DESCRIPTION = "A bot to look up homebrew info from a internet source. Written by zhu.exe#4211, modified by Dusk-Argentum#6530 and silverbass#2407." # Keep this the same.
TOKEN = #os.environ.get("TS")
UPDATE_DELAY = 600  # Delay is measured in seconds. "120" is 2 minutes, "360" is 6 minutes, "600" is 10 minutes, etc.

discordping = 1

# This is where your sources go.
EXAMPLE_CLASS_SOURCE = "" # Put your source URL between the quotes. Remember to use the RAW version if you're using GitHub.
EXAMPLE_FEAT_SOURCE = ""
EXAMPLE_ITEM_SOURCE = ""
EXAMPLE_MONSTER_SOURCE = ""
EXAMPLE_RACE_SOURCE = ""
EXAMPLE_SPELL_SOURCE = "" # Don't worry if you don't use them all; you can leave any one blank as long as you don't call it later.

# Source
SOURCE = "https://raw.githubusercontent.com/Dusk-Argentum/TomeSeeker-BETA/master/Sources.txt"

# Misadventures In Lyyth Sources
ADV_CLASS_SOURCE = "https://raw.githubusercontent.com/Dusk-Argentum/TomeSeeker/master/Misadventures%20in%20Lyyth/classes.txt"
ADV_FEAT_SOURCE = "https://raw.githubusercontent.com/Dusk-Argentum/TomeSeeker/master/Misadventures%20in%20Lyyth/feats.txt"
ADV_ITEM_SOURCE = "https://raw.githubusercontent.com/Dusk-Argentum/TomeSeeker/master/Misadventures%20in%20Lyyth/items.txt"
ADV_MONSTER_SOURCE = "https://raw.githubusercontent.com/Dusk-Argentum/TomeSeeker/master/Misadventures%20in%20Lyyth/monsters.txt"
ADV_RACE_SOURCE = "https://raw.githubusercontent.com/Dusk-Argentum/TomeSeeker/master/Misadventures%20in%20Lyyth/races.txt"
ADV_SPELL_SOURCE = "https://raw.githubusercontent.com/Dusk-Argentum/TomeSeeker/master/Misadventures%20in%20Lyyth/spells.txt"

# Planar Recovery And Improvement Mission Agency Sources
PRIMA_CLASS_SOURCE = "https://raw.githubusercontent.com/Dusk-Argentum/TomeSeeker/master/Planar%20Recovery%20and%20Improvement%20Mission%20Agency/classes.txt"
PRIMA_FEAT_SOURCE = "https://raw.githubusercontent.com/Dusk-Argentum/TomeSeeker/master/Planar%20Recovery%20and%20Improvement%20Mission%20Agency/feats.txt"
PRIMA_ITEM_SOURCE = "https://raw.githubusercontent.com/Dusk-Argentum/TomeSeeker/master/Planar%20Recovery%20and%20Improvement%20Mission%20Agency/items.txt"
PRIMA_MONSTER_SOURCE = "https://raw.githubusercontent.com/Dusk-Argentum/TomeSeeker/master/Planar%20Recovery%20and%20Improvement%20Mission%20Agency/monsters.txt"
PRIMA_RACE_SOURCE = "https://raw.githubusercontent.com/Dusk-Argentum/TomeSeeker/master/Planar%20Recovery%20and%20Improvement%20Mission%20Agency/races.txt"
PRIMA_SPELL_SOURCE = "https://raw.githubusercontent.com/Dusk-Argentum/TomeSeeker/master/Planar%20Recovery%20and%20Improvement%20Mission%20Agency/spells.txt"

# Keep these the same if you're following the example sources.
DIVIDER = "***"  # a string that divides distinct items.
IGNORED_ENTRIES = 1  # a number of entries to ignore (in case of an index, etc)
META_LINES = 0  # the number of lines of meta info each feat has

bot = commands.Bot(command_prefix=commands.when_mentioned_or(PREFIX), description=DESCRIPTION, pm_help=False) # Change "pm_help" to True if you want the help to be PMed instead of printed in the channel where the command is called.
client = discord.Client() # Leave this alone.

# If you ever decide to add more sources for different things, be sure to declare them here or else your bot will error out.
# Source
#sources = []
# ADV
adv_classes = []
adv_feats = []
adv_items = []
adv_monsters = []
adv_races = []
adv_spells = []
# PRIMA
prima_classes = []
prima_feats = []
prima_items = []
prima_monsters = []
prima_races = []
prima_spells = []

@bot.event
async def on_ready(): # What happens in this block happens upon startup. Be sure to include code to update your sources here.
	async with aiohttp.ClientSession() as session:
		async with session.get(ADV_CLASS_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update ADV classes: {text}")
			raw_adv_classes = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for adv_class in raw_adv_classes:
				lines = adv_class.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in adv_classes if name.lower() == i["name"].lower()]:
					adv_classes.remove(dup)
				adv_classes.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed class {name} from ADV.")
	async with aiohttp.ClientSession() as session:
		async with session.get(ADV_FEAT_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update ADV feats: {text}")
			raw_adv_feats = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for adv_feat in raw_adv_feats:
				lines = adv_feat.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in adv_feats if name.lower() == i["name"].lower()]:
					adv_feats.remove(dup)
				adv_feats.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed feat {name} from ADV.")
	async with aiohttp.ClientSession() as session:
		async with session.get(ADV_ITEM_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update ADV items: {text}")
			raw_adv_items = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for adv_item in raw_adv_items:
				lines = adv_item.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in adv_items if name.lower() == i["name"].lower()]:
					adv_items.remove(dup)
				adv_items.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed item {name} from ADV.")
	async with aiohttp.ClientSession() as session:
		async with session.get(ADV_MONSTER_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update ADV monsters: {text}")
			raw_adv_monsters = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for adv_monster in raw_adv_monsters:
				lines = adv_monster.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in adv_monsters if name.lower() == i["name"].lower()]:
					adv_monsters.remove(dup)
				adv_monsters.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed monster {name} from ADV.")
	async with aiohttp.ClientSession() as session:
		async with session.get(ADV_RACE_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update ADV races: {text}")
			raw_adv_races = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for adv_race in raw_adv_races:
				lines = adv_race.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in adv_races if name.lower() == i["name"].lower()]:
					adv_races.remove(dup)
				adv_races.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed race {name} from ADV.")
	async with aiohttp.ClientSession() as session:
		async with session.get(ADV_SPELL_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update ADV spells: {text}")
			raw_adv_spells = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for adv_spell in raw_adv_spells:
				lines = adv_spell.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in adv_spells if name.lower() == i["name"].lower()]:
					adv_spells.remove(dup)
				adv_spells.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed spell {name} from ADV.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_CLASS_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA classes: {text}")
			raw_prima_classes = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_class in raw_prima_classes:
				lines = prima_class.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_classes if name.lower() == i["name"].lower()]:
					prima_classes.remove(dup)
				prima_classes.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed class {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_FEAT_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA feats: {text}")
			raw_prima_feats = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_feat in raw_prima_feats:
				lines = prima_feat.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_feats if name.lower() == i["name"].lower()]:
					prima_feats.remove(dup)
				prima_feats.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed feat {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_ITEM_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA items: {text}")
			raw_prima_items = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_item in raw_prima_items:
				lines = prima_item.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_items if name.lower() == i["name"].lower()]:
					prima_items.remove(dup)
				prima_items.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed item {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_MONSTER_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA monsters: {text}")
			raw_prima_monsters = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_monster in raw_prima_monsters:
				lines = prima_monster.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_monsters if name.lower() == i["name"].lower()]:
					prima_monsters.remove(dup)
				prima_monsters.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed monster {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_RACE_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA races: {text}")
			raw_prima_races = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_race in raw_prima_races:
				lines = prima_race.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_races if name.lower() == i["name"].lower()]:
					prima_races.remove(dup)
				prima_races.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed race {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_SPELL_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA spells: {text}")
			raw_prima_spells = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_spell in raw_prima_spells:
				lines = prima_spell.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_spells if name.lower() == i["name"].lower()]:
					prima_spells.remove(dup)
				prima_spells.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed spell {name} from PRIMA.")
	await bot.change_presence(game=discord.Game(name="D&D 5e | .help"), status=discord.Status("online")) # This line sets the bot's presence upon startup. Change the prefix to match the one above, or change the whole message entirely. It's up to you.
	bot.loop.create_task(update_sources_loop())
	await bot.change_presence(game=discord.Game(name="D&D 5e | .help"), status=discord.Status("online")) # This line sets the bot's presence upon startup. Change the prefix to match the one above, or change the whole message entirely. It's up to you.
	bot.loop.create_task(update_sources_loop())

@bot.event # This sends errors when necessary.
async def on_command_error(error, ctx):
	if isinstance(error, commands.CommandNotFound):
		return
	if isinstance(error, CommandInvokeError):
		error = error.original
	await bot.send_message(ctx.message.channel, error)
	
@bot.event # This updates the sources at the interval mentioned at the beginning.
async def update_sources_loop():
	try:
		await bot.wait_until_ready()
		while not bot.is_closed:
			await update_sources()
			await asyncio.sleep(UPDATE_DELAY)
	except asyncio.CancelledError:
		pass
		
async def update_sources(): # This is required to update your sources at a regular interval so you don't have to restart your bot/force an update via the ".update" command every time you add something new. Be sure to change everything to your sources.
	async with aiohttp.ClientSession() as session:
		async with session.get(ADV_CLASS_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update ADV classes: {text}")
			adv_classes.clear()
			raw_adv_classes = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for adv_class in raw_adv_classes:
				lines = adv_class.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in adv_classes if name.lower() == i["name"].lower()]:
					adv_classes.remove(dup)
				adv_classes.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed class {name} from ADV.")
	async with aiohttp.ClientSession() as session:
		async with session.get(ADV_FEAT_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update ADV feats: {text}")
			adv_feats.clear()
			raw_adv_feats = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for adv_feat in raw_adv_feats:
				lines = adv_feat.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in adv_feats if name.lower() == i["name"].lower()]:
					adv_feats.remove(dup)
				adv_feats.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed feat {name} from ADV.")
	async with aiohttp.ClientSession() as session:
		async with session.get(ADV_ITEM_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update ADV items: {text}")
			adv_items.clear()
			raw_adv_items = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for adv_item in raw_adv_items:
				lines = adv_item.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in adv_items if name.lower() == i["name"].lower()]:
					adv_items.remove(dup)
				adv_items.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed item {name} from ADV.")
	async with aiohttp.ClientSession() as session:
		async with session.get(ADV_MONSTER_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update ADV monsters: {text}")
			adv_monsters.clear()
			raw_adv_monsters = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for adv_monster in raw_adv_monsters:
				lines = adv_monster.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in adv_monsters if name.lower() == i["name"].lower()]:
					adv_monsters.remove(dup)
				adv_monsters.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed monster {name} from ADV.")
	async with aiohttp.ClientSession() as session:
		async with session.get(ADV_RACE_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update ADV races: {text}")
			adv_races.clear()
			raw_adv_races = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for adv_race in raw_adv_races:
				lines = adv_race.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in adv_races if name.lower() == i["name"].lower()]:
					adv_races.remove(dup)
				adv_races.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed race {name} from ADV.")
	async with aiohttp.ClientSession() as session:
		async with session.get(ADV_SPELL_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update ADV spells: {text}")
			adv_spells.clear()
			raw_adv_spells = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for adv_spell in raw_adv_spells:
				lines = adv_spell.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in adv_spells if name.lower() == i["name"].lower()]:
					adv_spells.remove(dup)
				adv_spells.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed spell {name} from ADV.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_CLASS_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA classes: {text}")
			prima_classes.clear()
			raw_prima_classes = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_class in raw_prima_classes:
				lines = prima_class.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_classes if name.lower() == i["name"].lower()]:
					prima_classes.remove(dup)
				prima_classes.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed class {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_FEAT_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA feats: {text}")
			prima_feats.clear()
			raw_prima_feats = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_feat in raw_prima_feats:
				lines = prima_feat.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_feats if name.lower() == i["name"].lower()]:
					prima_feats.remove(dup)
				prima_feats.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed feat {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_ITEM_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA items: {text}")
			prima_items.clear()
			raw_prima_items = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_item in raw_prima_items:
				lines = prima_item.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_items if name.lower() == i["name"].lower()]:
					prima_items.remove(dup)
				prima_items.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed item {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_MONSTER_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA monsters: {text}")
			prima_monsters.clear()
			raw_prima_monsters = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_monster in raw_prima_monsters:
				lines = prima_monster.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_monsters if name.lower() == i["name"].lower()]:
					prima_monsters.remove(dup)
				prima_monsters.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed monster {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_RACE_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA races: {text}")
			prima_races.clear()
			raw_prima_races = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_race in raw_prima_races:
				lines = prima_race.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_races if name.lower() == i["name"].lower()]:
					prima_races.remove(dup)
				prima_races.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed race {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_SPELL_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA spells: {text}")
			prima_spells.clear()
			raw_prima_spells = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_spell in raw_prima_spells:
				lines = prima_spell.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_spells if name.lower() == i["name"].lower()]:
					prima_spells.remove(dup)
				prima_spells.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed spell {name} from PRIMA.")
			
async def is_owner(ctx):
    return ctx.author.id == 97153790897045504

@bot.event
async def dis():
	async with aiohttp.get("http://discord.gg/") as r:
		discordping == 1
		if discordping == 1:
			channels = bot.get_all_channels()
			print(f"I just pinged Discord so I don't die!")
			asyncio.sleep(50)
			
@bot.group(pass_context=True, name="sources", aliases=["srcs"])
async def sources(ctx):
	if ctx.invoked_subcommand is None:
		await bot.say("Please specify the type of content you are looking for. Valid arguments: `class`, `feat`, `item`, `monster`, `race`, `spell`.")
@sources.command(pass_context=True, name="_class", aliases=["class"])
async def _class(ctx):
	embed = EmbedWithAuthor(ctx)
	embed.title = "Class Sources"
	embed.description = "Lists the source of the classes and then the classes themselves as they are invoked, then the command to list them all."
	embed.add_field(name="ADV", value="`.class adv`")
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
@sources.command(pass_context=True)
async def feat(ctx):
	embed = EmbedWithAuthor(ctx)
	embed.title = "Feat Sources"
	embed.description = "Lists the source of the feats as they are invoked, then the command to list them all."
	embed.add_field(name="ADV", value="`.feat adv`")
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
@sources.command(pass_context=True)
async def item(ctx):
	embed = EmbedWithAuthor(ctx)
	embed.title = "Item Sources"
	embed.description = "Lists the source of the items as they are invoked, then the command to list them all."
	embed.add_field(name="ADV", value="~~`.item adv`~~ This list isn't quite working, but that doesn't matter right now, cuz there's nothing in it anyway!")
	embed.add_field(name="PRIMA", value="~~`.item prima`~~ This list isn't quite working, but that doesn't matter right now, cuz there's nothing in it anyway!")
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
@sources.command(pass_context=True)
async def monster(ctx):
	embed = EmbedWithAuthor(ctx)
	embed.title = "Monster Sources"
	embed.description = "Lists the source of the monsters as they are invoked, then the command to list them all."
	embed.add_field(name="Unfortunately, this is empty.", value=":(")
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
@sources.command(pass_context=True)
async def race(ctx):
	embed = EmbedWithAuthor(ctx)
	embed.title = "Race Sources"
	embed.description = "Lists the source of the races as they are invoked, then the command to list them all."
	embed.add_field(name="Unfortunately, this is empty.", value=":(")
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
@sources.command(pass_context=True)
async def spell(ctx):
	embed = EmbedWithAuthor(ctx)
	embed.title = "Spell Sources"
	embed.description = "Lists the source of spells as they are invoked, then the command to list them all."
	embed.add_field(name="PRIMA", value="~~`.spell prima`~~ This one isn't quite working, but there's nothing here anyway.")
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
	
@bot.group(pass_context=True, name="_class2", aliases=["class2"])
async def _class2(ctx):
	if ctx.invoked_subcommand is None:
		await bot.say("You need to enter a class. See full supported list with `.sources class`.")	
@_class2.command(pass_context=True, name="_adv", aliases=["adv"])
async def adv(ctx, *, name=""):
	result = search(adv_classes, 'name', name)
	if result is None:
		return await bot.say('Class not found.')
	strict = result[1]
	results = result[0]
	if strict:
		result = results
	else:
		if len(results) == 1:
			result = results[0]
		else:
			result = await get_selection(ctx, [(r['name'], r) for r in results])
			if result is None: return await bot.say('Selection timed out or was cancelled.')
	meta = result["meta"]
	meta2 = [meta[i:i + 1024] for i in range(2048, len(meta), 1024)]
	lines = meta.split("\n")
	embed = EmbedWithAuthor(ctx)
	embed.title = lines[0]
	embed.add_field(name="Level-Up Table", value=lines[1:5])
	#embed.add_field(name="Hit Die", value=lines[40], inline=False)
	#embed.add_field(name="Saving Throws", value=lines[41], inline=True)
	#embed.add_field(name="Starting Proficiencies", value=lines[42])
	#embed.add_field(name="Starting Equipment", value=lines[43])
	#embed.set_thumbnail(url=lines[6])
	for piece in meta2:
		embed.add_field(name="\u200b", value=piece)
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
@_class2.command(pass_context=True, name="_prima", aliases=["prima"])
async def prima(ctx, *, name=""):
	result = search(prima_classes, 'name', name)
	if result is None:
		return await bot.say('Class not found.')
	strict = result[1]
	results = result[0]
	if strict:
		result = results
	else:
		if len(results) == 1:
			result = results[0]
		else:
			result = await get_selection(ctx, [(r['name'], r) for r in results])
			if result is None: return await bot.say('Selection timed out or was cancelled.')
	meta = result["meta"]
	meta2 = [meta[i:i + 1024] for i in range(2048, len(meta), 1024)]
	lines = meta.split("\n")
	embed = EmbedWithAuthor(ctx)
	embed.title = "WIP, please be patient."
	#embed.title = lines[0]
	#embed.add_field(name="Level-Up Table", value=lines[1:5])
	#embed.add_field(name="Hit Die", value=lines[40], inline=False)
	#embed.add_field(name="Saving Throws", value=lines[41], inline=True)
	#embed.add_field(name="Starting Proficiencies", value=lines[42])
	#embed.add_field(name="Starting Equipment", value=lines[43])
	#embed.set_thumbnail(url=lines[6])
	for piece in meta2:
		embed.add_field(name="\u200b", value=piece)
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
	
@bot.group(pass_context=True)
async def feat(ctx):
	if ctx.invoked_subcommand is None:
		await bot.say("You need to enter a valid source. See full supported list with `.sources feat`.")
@feat.command(pass_context=True)
async def adv(ctx, *, name=""):
	result = search(adv_feats, "name", name)
	if result is None:
		return await bot.say("Feat not found.")
	strict = result[1]
	results = result[0]
	if strict:
		result = results
	else:
		if len(results) == 1:
			result = results[0]
		else:
			result = await get_selection(ctx, [(r["name"], r) for r in results])
			if result is None: return await bot.say("Selection timed out or was cancelled.")
	embed = EmbedWithAuthor(ctx)
	embed.title = result["name"]
	meta = result["meta"]
	if "*Prerequisite: " in meta:
		prereq = meta[len("*Prerequisite: ")+meta.find("*Prerequisite: "):meta.find("*\n")]
		meta = meta[(meta.find("*\n")+2)::]
		embed.add_field(name="Prerequisite", value=prereq)
	embed.add_field(name="Source", value="Adventurer")
	if ("Increase your " in meta and " score by 1, up to a maximum of 20." in meta):
		hasi = meta[meta.find("Increase your "):meta.find("up to a maximum of 20.\n")+len("up to a maximum of 20.\n")]
		meta = meta[(meta.find("up to a maximum of 20.\n")+len("up to a maximum of 20.\n"))::]
		embed.add_field(name="Ability Improvement", value=hasi)
	embed.add_field(name="Description", value=meta[0:1024])
	meta2 = [meta[i:i + 1024] for i in range(1024, len(meta), 1024)]
	for piece in meta2:
		embed.add_field(name="\u200b", value=piece)
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
@feat.command(pass_context=True)
async def prima(ctx, *, name=""):
	result = search(prima_feats, "name", name)
	if result is None:
		return await bot.say("Feat not found.")
	strict = result[1]
	results = result[0]
	if strict:
		result = results
	else:
		if len(results) == 1:
			result = results[0]
		else:
			result = await get_selection(ctx, [(r["name"], r) for r in results])
			if result is None: return await bot.say("Selection timed out or was cancelled.")
	embed = EmbedWithAuthor(ctx)
	embed.title = result["name"]
	meta = result["meta"]
	meta2 = [meta[i:i + 1024] for i in range(2048, len(meta), 1024)]
	embed.description = meta[0:2048]
	for piece in meta2:
		embed.add_field(name="\u200b", value=piece)
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
	
@bot.group(pass_context=True)
async def item(ctx):
	if ctx.invoked_subcommand is None:
		await bot.say("You need to enter a valid source. See full supported list with `.sources item`.")
@item.command(pass_context=True)
async def adv(ctx, *, name=""):
	result = search(adv_items, "name", name)
	if result is None:
		return await bot.say("Item not found.")
	strict = result[1]
	results = result[0]
	if strict:
		result = results
	else:
		if len(results) == 1:
			result = results[0]
		else:
			result = await get_selection(ctx, [(r["name"], r) for r in results])
			if result is None: return await bot.say("Selection timed out or was cancelled.")
	embed = EmbedWithAuthor(ctx)
	embed.title = result["name"]
	meta = result["meta"]
	meta2 = [meta[i:i + 1024] for i in range(2048, len(meta), 1024)]
	lines = meta.split("\n")
	embed.description = lines[0]
	embed.add_field(name="Description", value=lines[1])
	for piece in meta2:
		embed.add_field(name="\u200b", value=piece)
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
@item.command(pass_context=True)
async def prima(ctx, *, name=""):
	result = search(prima_items, "name", name)
	if result is None:
		return await bot.say("Item not found.")
	strict = result[1]
	results = result[0]
	if strict:
		result = results
	else:
		if len(results) == 1:
			result = results[0]
		else:
			result = await get_selection(ctx, [(r["name"], r) for r in results])
			if result is None: return await bot.say("Selection timed out or was cancelled.")
	embed = EmbedWithAuthor(ctx)
	meta = result["meta"]
	meta2 = [meta[i:i + 1024] for i in range(2048, len(meta), 1024)]
	lines = meta.split("\n")
	embed.title = result["name"]
	embed.description = lines[0]
	#embed.add_field(name="Description", value=lines[1])
	for piece in meta2:
		embed.add_field(name="\u200b", value=piece)
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
	
@bot.group(pass_context=True)
async def monster(ctx):
	if ctx.invoked_subcommand is None:
		await bot.say("You need to enter a valid source. See full supported list with `.sources monster`.")
@monster.command(pass_context=True)
async def adv(ctx, *, name=""):
	result = search(adv_monsters, "name", name)
	if result is None:
		return await bot.say("Monster not found.")
	strict = result[1]
	results = result[0]
	if strict:
		result = results
	else:
		if len(results) == 1:
			result = results[0]
		else:
			result = await get_selection(ctx, [(r["name"], r) for r in results])
			if result is None: return await bot.say("Selection timed out or was cancelled.")
	embed = EmbedWithAuthor(ctx)
	embed.title = result["name"]
	meta = result["meta"]
	meta2 = [meta[i:i + 1024] for i in range(2048, len(meta), 1024)]
	lines = meta.split("\n")
	embed.description = lines[0]
	#embed.description = meta[0:0]
	embed.add_field(name="Info", value=lines[1])
	#embed.add_field(name="Info", value=meta[1:1])
	embed.set_thumbnail(url=meta[2:2])
	for piece in meta2:
		embed.add_field(name="\u200b", value=piece)
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
@monster.command(pass_context=True)
async def prima(ctx, *, name=""):
	result = search(prima_monsters, "name", name)
	if result is None:
		return await bot.say("Monster not found.")
	strict = result[1]
	results = result[0]
	if strict:
		result = results
	else:
		if len(results) == 1:
			result = results[0]
		else:
			result = await get_selection(ctx, [(r["name"], r) for r in results])
			if result is None: return await bot.say("Selection timed out or was cancelled.")
	embed = EmbedWithAuthor(ctx)
	embed.title = result["name"]
	meta = result["meta"]
	meta2 = [meta[i:i + 1024] for i in range(2048, len(meta), 1024)]
	#lines = meta.split("\n")
	#embed.description = lines[0:0]
	embed.description = meta[0:0]
	#embed.add_field(name="Info", value=lines[1:1])
	embed.add_field(name="Info", value=meta[1:1])
	#embed.set_thumbnail(url=meta[2:2])
	for piece in meta2:
		embed.add_field(name="\u200b", value=piece)
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
	
@bot.group(pass_context=True)
async def race(ctx):
	if ctx.invoked_subcommand is None:
		await bot.say("You need to enter a valid source. See full supported list with `.sources race`.")
@race.command(pass_context=True)
async def adv(ctx, *, name=""):
	result = search(adv_races, "name", name)
	if result is None:
		return await bot.say("Race not found.")
	strict = result[1]
	results = result[0]
	if strict:
		result = results
	else:
		if len(results) == 1:
			result = results[0]
		else:
			result = await get_selection(ctx, [(r["name"], r) for r in results])
			if result is None: return await bot.say("Selection timed out or was cancelled.")
	embed = EmbedWithAuthor(ctx)
	embed.title = result["name"]
	meta = result["meta"]
	meta2 = [meta[i:i + 1024] for i in range(2048, len(meta), 1024)]
	embed.description = meta[0:2048]
	for piece in meta2:
		embed.add_field(name="\u200b", value=piece)
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
@race.command(pass_context=True)
async def prima(ctx, *, name=""):
	result = search(prima_races, "name", name)
	if result is None:
		return await bot.say("Race not found.")
	strict = result[1]
	results = result[0]
	if strict:
		result = results
	else:
		if len(results) == 1:
			result = results[0]
		else:
			result = await get_selection(ctx, [(r["name"], r) for r in results])
			if result is None: return await bot.say("Selection timed out or was cancelled.")
	embed = EmbedWithAuthor(ctx)
	embed.title = result["name"]
	meta = result["meta"]
	meta2 = [meta[i:i + 1024] for i in range(2048, len(meta), 1024)]
	embed.description = meta[0:2048]
	for piece in meta2:
		embed.add_field(name="\u200b", value=piece)
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)

@bot.group(pass_context=True)
async def spell(ctx):
	if ctx.invoked_subcommand is None:
		await bot.say("You need to enter a valid source. See full supported list with `.sources spell`.")
@spell.command(pass_context=True)
async def adv(ctx, *, name=""):
	result = search(adv_spells, "name", name)
	if result is None:
		return await bot.say("Spell not found.")
	strict = result[1]
	results = result[0]
	if strict:
		result = results
	else:
		if len(results) == 1:
			result = results[0]
		else:
			result = await get_selection(ctx, [(r["name"], r) for r in results])
			if result is None: return await bot.say("Selection timed out or was cancelled.")
	embed = EmbedWithAuthor(ctx)
	embed.title = result["name"]
	meta = result["meta"]
	meta2 = [meta[i:i + 1024] for i in range(2048, len(meta), 1024)]
	embed.description = meta[0:2048]
	for piece in meta2:
		embed.add_field(name="\u200b", value=piece)
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
@spell.command(pass_context=True)
async def prima(ctx, *, name=""):
	result = search(prima_spells, "name", name)
	if result is None:
		return await bot.say("Spell not found.")
	strict = result[1]
	results = result[0]
	if strict:
		result = results
	else:
		if len(results) == 1:
			result = results[0]
		else:
			result = await get_selection(ctx, [(r["name"], r) for r in results])
			if result is None: return await bot.say("Selection timed out or was cancelled.")
	embed = EmbedWithAuthor(ctx)
	embed.title = result["name"]
	meta = result["meta"]
	meta2 = [meta[i:i + 1024] for i in range(2048, len(meta), 1024)]
	lines = meta.split("\n")
	embed.description = lines[0]
	for piece in meta2:
		embed.add_field(name="\u200b", value=piece)
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)
	
@bot.command(pass_context=True, name="_class", aliases=["class"]) # This is the classes command.
async def _class(ctx, *, name=""):
	embed = EmbedWithAuthor(ctx)
	embed.title = "Adventurer Version 1.5"
	embed.add_field(name="Level-Up Table", value="`1` Feat, Feat, Feat, Feat\n\
`2` Feat, Feat\n\
`3` Feat\n\
`4` Ability Score Improvement, Feat\n\
`5` Feat\n\
`6` Ability Score Improvement, Feat\n\
`7` Feat\n\
`8` Ability Score Improvement, Feat\n\
`9` Feat\n\
`10` Ability Score Improvement, Feat\n\
`11` Feat\n\
`12` Ability Score Improvement, Feat\n\
`13` Feat\n\
`14` Ability Score Improvement, Feat\n\
`15` Feat\n\
`16` Ability Score Improvement, Feat\n\
`17` Feat\n\
`18` Feat\n\
`19` Ability Score Improvement, Feat\n\
`20` Feat, Feat")
	embed.add_field(name="Hit Die", value="1d8", inline=False)
	embed.add_field(name="Saving Throws", value="None.")
	embed.add_field(name="Starting Proficiencies", value="You are proficient with nothing except for any proficiencies provided by your race or background. \n\
You must pick up armor, weapon, tool, skill, and saving throw proficiencies through feats.")
	embed.add_field(name="Starting Equipment", value="You start with the equipment provided by your background, as well as 4d4 x 10 gp to buy your own equipment.")
	embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/348897378062827520/425406341788467210/68747470733a2f2f6765656b616e6473756e6472792e636f6d2f77702d636f6e74656e742f75706c6f6164732f323031362f.jpg")
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)

@bot.command(pass_context=True, name="update", aliases=["u"])
async def update(ctx, *, name=""):
	adv_classes.clear()
	adv_feats.clear()
	adv_items.clear()
	adv_monsters.clear()
	adv_races.clear()
	adv_spells.clear()
	prima_classes.clear()
	prima_feats.clear()
	prima_items.clear()
	prima_monsters.clear()
	prima_races.clear()
	prima_spells.clear()
	async with aiohttp.ClientSession() as session:
		async with session.get(ADV_CLASS_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update ADV classes: {text}")
			raw_adv_classes = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for adv_class in raw_adv_classes:
				lines = adv_class.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in adv_classes if name.lower() == i["name"].lower()]:
					adv_classes.remove(dup)
				adv_classes.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed class {name} from ADV.")
	async with aiohttp.ClientSession() as session:
		async with session.get(ADV_FEAT_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update ADV feats: {text}")
			raw_adv_feats = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for adv_feat in raw_adv_feats:
				lines = adv_feat.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in adv_feats if name.lower() == i["name"].lower()]:
					adv_feats.remove(dup)
				adv_feats.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed feat {name} from ADV.")
	async with aiohttp.ClientSession() as session:
		async with session.get(ADV_ITEM_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update ADV items: {text}")
			raw_adv_items = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for adv_item in raw_adv_items:
				lines = adv_item.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in adv_items if name.lower() == i["name"].lower()]:
					adv_items.remove(dup)
				adv_items.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed item {name} from ADV.")
	async with aiohttp.ClientSession() as session:
		async with session.get(ADV_MONSTER_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update ADV monsters: {text}")
			raw_adv_monsters = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for adv_monster in raw_adv_monsters:
				lines = adv_monster.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in adv_monsters if name.lower() == i["name"].lower()]:
					adv_monsters.remove(dup)
				adv_monsters.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed monster {name} from ADV.")
	async with aiohttp.ClientSession() as session:
		async with session.get(ADV_RACE_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update ADV races: {text}")
			raw_adv_races = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for adv_race in raw_adv_races:
				lines = adv_race.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in adv_races if name.lower() == i["name"].lower()]:
					adv_races.remove(dup)
				adv_races.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed race {name} from ADV.")
	async with aiohttp.ClientSession() as session:
		async with session.get(ADV_SPELL_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update ADV spells: {text}")
			raw_adv_spells = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for adv_spell in raw_adv_spells:
				lines = adv_spell.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in adv_spells if name.lower() == i["name"].lower()]:
					adv_spells.remove(dup)
				adv_spells.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed spell {name} from ADV.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_CLASS_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA classes: {text}")
			raw_prima_classes = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_class in raw_prima_classes:
				lines = prima_class.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_classes if name.lower() == i["name"].lower()]:
					prima_classes.remove(dup)
				prima_classes.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed class {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_FEAT_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA feats: {text}")
			raw_prima_feats = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_feat in raw_prima_feats:
				lines = prima_feat.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_feats if name.lower() == i["name"].lower()]:
					prima_feats.remove(dup)
				prima_feats.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed feat {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_ITEM_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA items: {text}")
			raw_prima_items = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_item in raw_prima_items:
				lines = prima_item.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_items if name.lower() == i["name"].lower()]:
					prima_items.remove(dup)
				prima_items.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed item {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_MONSTER_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA monsters: {text}")
			raw_prima_monsters = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_monster in raw_prima_monsters:
				lines = prima_monster.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_monsters if name.lower() == i["name"].lower()]:
					prima_monsters.remove(dup)
				prima_monsters.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed monster {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_RACE_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA races: {text}")
			raw_prima_races = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_race in raw_prima_races:
				lines = prima_race.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_races if name.lower() == i["name"].lower()]:
					prima_races.remove(dup)
				prima_races.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed race {name} from PRIMA.")
	async with aiohttp.ClientSession() as session:
		async with session.get(PRIMA_SPELL_SOURCE) as resp:
			text = await resp.text()
			if 399 < resp.status < 600:
				raise Exception(f"Failed to update PRIMA spells: {text}")
			raw_prima_spells = [t.strip() for t in text.split(DIVIDER)][IGNORED_ENTRIES:]
			for prima_spell in raw_prima_spells:
				lines = prima_spell.split("\n")
				name = lines[0].strip("# ")
				meta = "\n".join(lines[1::])
				desc = "\n".join(lines)
				for dup in [i for i in prima_spells if name.lower() == i["name"].lower()]:
					prima_spells.remove(dup)
				prima_spells.append({"name": name, "meta": meta, "desc": desc})
				print(f"Indexed spell {name} from PRIMA.")
			await bot.add_reaction(ctx.message, emoji="\N{THUMBS UP SIGN}")
			
@bot.command()
async def echo(*, message: str):
	await bot.say(message)
	
@bot.command(pass_context=True)
@commands.check(is_owner)
async def e(ctx, message: str):
	await bot.say(message)
	await bot.delete_message(ctx.message)
	
@bot.command(pass_context=True)
async def remind(ctx, message: str, input: int):
	if input is None:
		await bot.say("You forgot to input a time.")
	else:
		await bot.say("Reminder set!")
		await bot.delete_message(ctx.message)
		await asyncio.sleep(input)
		await bot.say(ctx.message.author.mention+": "+message)

@bot.command(pass_context=True)
async def help(ctx, *, name=""):
	embed = EmbedWithAuthor(ctx)
	embed.title = "TomeSeeker: Version 1.2 | Commands"
	embed.add_field(name="Lookup", value="`.sources` \n\
Lists the types of sources, in which you can find the abbreviations required to perform the lookup commands below. \n\
`.class [source]` \n\
Lists the classes in [source]. Do `.class [source] [class]` for detailed info on [class]. \n\
`.feat [source]` \n\
Lists the feats in [source]. Do `.feat [source] [feat]` for detailed info on [feat]. \n\
`.item [source]` \n\
Lists the items in [source]. Do `.item [source] [item]` for detailed info on [item]. \n\
`.monster [source]` \n\
Lists the monsters in [source]. Do `.monster [source] [monster]` for detailed info on [monster]. \n\
`.race [source]` \n\
Lists the races in [source]. Do `.race [source] [race]` for detailed info on [race]. \n\
`.spell [source]` \n\
Lists the spells in [source]. Do `.spell [source] [spell]` for detailed info on [spell].")
	embed.add_field(name="Miscellaneous", value="`.update` {Alias: `.u`} \n\
Forces an update of the Class, Feat, Item, Monster, Race, and Spell databases.")
	embed.add_field(name="For Fun", value="`.echo [message]` \n\
Echoes back [message]. \n\
`.remind [message] [seconds]` \n\
Reminds you of [message] in [seconds]. NOTE: ALL reminders will be indiscriminately CLEARED in the event of a bot restart.")
	embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/348897378062827520/425306674006327307/Compass.png")
	embed.set_footer(text="Lovingly (at times) crafted by Dusk-Argentum#6530. | Please note TomeSeeker is constantly in development! Some things may not work as expected.")
	await bot.say(embed=embed)
	await bot.delete_message(ctx.message)

@bot.event
async def on_message(message):
	if message.content.startswith("Reminder set!"):
		await asyncio.sleep(15)
		await bot.delete_message(message)
	if message.content.startswith(".remind"):
		await asyncio.sleep(10)
		await bot.delete_message(message)
	if message.content.startswith("A"):
		print("Pinged Discord.")
	await bot.process_commands(message)
	
bot.run(TOKEN)
