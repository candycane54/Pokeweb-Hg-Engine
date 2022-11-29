import ndspy
import ndspy.rom
import ndspy.narc
import code 
import io
import os
import os.path
from os import path
import json
import copy

# code.interact(local=dict(globals(), **locals()))

######################### FILE SPECIFIC CONSTANTS #############################

def set_global_vars():
	global ROM_NAME, TYPES, EGG_GROUPS, GROWTHS, ABILITIES, ITEMS, POKEDEX, PERSONAL_NARC_FORMAT
	

	with open(f'session_settings.json', "r") as outfile:  
		settings = json.load(outfile) 
		ROM_NAME = settings['rom_name']

	TYPES = ["Normal", "Fighting", "Flying", "Poison", "Ground", "Rock", "Bug", "Ghost", "Steel","Mystery", "Fire", "Water","Grass","Electric","Psychic","Ice","Dragon","Dark"]


	EGG_GROUPS = ["~","Monster","Water 1","Bug","Flying","Field","Fairy","Grass","Human-Like","Water 3","Mineral","Amorphous","Water 2","Ditto","Dragon","Undiscovered"];
	GROWTHS = ["Medium Fast","Erratic","Fluctuating","Medium Slow","Fast","Slow","Medium Fast","Medium Fast"]
	ABILITIES = open(f'texts/abilities.txt', "r").read().splitlines() 
	ITEMS = open(f'texts/items.txt', mode="r").read().splitlines()
	POKEDEX = open(f'texts/pokedex.txt', "r").read().splitlines()

	PERSONAL_NARC_FORMAT = [[1, "base_hp"],
	[1,	"base_atk"],
	[1,	"base_def"],
	[1,	"base_speed"],
	[1,	"base_spatk"],
	[1,	"base_spdef"],
	[1,	"type_1"],
	[1,	"type_2"],
	[1,	"catchrate"],
	[1,	"base_exp"],
	[2,	"evs"],
	[2,	"item_1"],
	[2,	"item_2"],
	[1,	"gender"],
	[1,	"hatch_cycle"],
	[1,	"base_happy"],
	[1,	"exp_rate"],
	[1,	"egg_group_1"],
	[1,	"egg_group_2"],
	[1,	"ability_1"],
	[1,	"ability_2"],
	[1,	"flee"],
	[3,	"color"],
	[4, "tm_1-32"],
	[4, "tm_33-64"],
	[4, "tm_65-95+hm_1"],
	[4, "hm_2-6"]]





#################################################################


def output_personal_json(narc):
	set_global_vars()
	data_index = 0
	
	# while len(narc.files) < 800:
	# 	narc.files.append(narc.files[-2])

	for data in narc.files:
		data_name = data_index
		read_narc_data(data, PERSONAL_NARC_FORMAT, data_name)
		data_index += 1

def read_narc_data(data, narc_format, file_name):
	stream = io.BytesIO(data)
	pokemon = {"raw": {}, "readable": {} }
	#USE THE FORMAT LIST TO PARSE BYTES
	for entry in narc_format: 
		pokemon["raw"][entry[1]] = read_bytes(stream, entry[0])

	#CONVERT TO READABLE FORMAT USING CONSTANTS/TEXT BANKS
	pokemon["readable"] = to_readable(pokemon["raw"], file_name)
	
	#OUTPUT TO JSON
	if not os.path.exists(f'{ROM_NAME}/json/personal'):
		os.makedirs(f'{ROM_NAME}/json/personal')

	with open(f'{ROM_NAME}/json/personal/{file_name}.json', "w") as outfile:  
		json.dump(pokemon, outfile) 


def to_readable(raw, file_name):
	readable = copy.deepcopy(raw)

	readable["index"] = file_name
	
	gen = "6"
	if file_name <= 151:
		gen = "1"
	elif file_name <= 251:
		gen = "2"
	elif file_name <= 386:
		gen = "3"
	elif file_name <= 493:
		gen = "4"
	elif file_name <= 649:
		gen = "5"
	else:
		gen = "6"
	readable["gen"] = gen




	try:
		readable["name"] = POKEDEX[file_name].upper()
	except IndexError:
		readable["name"] = "Alt Form"

	try:
		readable["type_1"] = TYPES[raw["type_1"]]
	except IndexError:
		return

	readable["type_2"] = TYPES[raw["type_2"]]

	try:

		readable["item_1"] = ITEMS[raw["item_1"]]
		readable["item_2"] = ITEMS[raw["item_2"]]
		readable["exp_rate"] = GROWTHS[raw["exp_rate"]]
	except IndexError:
		code.interact(local=dict(globals(), **locals()))

	

	readable["egg_group_1"] = EGG_GROUPS[raw["egg_group_1"]]
	readable["egg_group_2"] = EGG_GROUPS[raw["egg_group_2"]]

	readable["ability_1"] = ABILITIES[raw["ability_1"]]
	readable["ability_2"] = ABILITIES[raw["ability_2"]]
	readable["ability_3"] = ABILITIES[0]


	readable["form_sprites"] = "Default"

	binary_ev = bin(raw["evs"])[2:].zfill(16) 
	index = 16
	ev_yields = ["hp_yield", "atk_yield", "def_yield", "speed_yield", "spatk_yield", "spdef_yield"]

	for ev in ev_yields:
		amount = int(binary_ev[index-2:index],2)
		readable[ev] = amount
		index -= 2

	return readable

def read_bytes(stream, n):
	return int.from_bytes(stream.read(n), 'little')

	
