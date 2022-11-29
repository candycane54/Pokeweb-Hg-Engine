import ndspy
import ndspy.rom
import ndspy.narc
import code 
import io
import os
import json
import copy
import sys


# code.interact(local=dict(globals(), **locals()))

######################### CONSTANTS #############################
def set_global_vars():
	global ROM_NAME, NARC_FORMAT, NARC_FILE_ID, TRAINER_CLASSES, ITEMS, BATTLE_TYPES, TRAINER_NAMES, AIS, TEMPLATE_FLAGS
	
	with open(f'session_settings.json', "r") as outfile:  
		settings = json.load(outfile) 
		ROM_NAME = settings['rom_name']
		NARC_FILE_ID = settings['trdata']

	TEMPLATE_FLAGS =["has_moves", "has_items", "set_abilities", "set_ball", "set_iv_ev", "set_nature", "shiny_lock", "additional_flags"]

	TRAINER_CLASSES = open(f'texts/tr_classes.txt', "r").read().splitlines()
	TRAINER_NAMES = open(f'texts/tr_names.txt', "r").read().splitlines()
	ITEMS = open(f'texts/items.txt', mode="r").read().splitlines()
	BATTLE_TYPES = ["Singles", "Doubles"]

	TRPOK_INFO = []

	AIS = ["Prioritize Effectiveness",
	"Evaluate Attacks",
	"Expert",
	"Prioritize Status",
	"Risky Attacks",
	"Prioritize Damage",
	"Partner",
	"Double Battle",
	"Prioritize Healing",
	"Utilize Weather",
	"Harassment",
	"Roaming Pokemon",
	"Safari Zone",
	"Catching Demo"]

	NARC_FORMAT = [[1, "template"],
	[1, "class"],
	[1, "battle_type"],
	[1, "num_pokemon"],
	[2, "item_1"],
	[2, "item_2"],
	[2, "item_3"],
	[2, "item_4"],
	[4, "ai"],
	[1, "battle_type_2"]]

set_global_vars()
#################################################################

## TODO instead of opening and editing the entire narc repeatedly, edit a variable 
## and edit the narc just once

def output_narc(narc_name="trdata"):
	json_files = os.listdir(f'{ROM_NAME}/json/{narc_name}')
	narcfile_path = f'{ROM_NAME}/narcs/{narc_name}-{NARC_FILE_ID}.narc'
	
	# ndspy copy of narcfile to edit
	narc = ndspy.narc.NARC.fromFile(narcfile_path)

	for f in json_files:
		file_name = int(f.split(".")[0])

		write_narc_data(file_name, NARC_FORMAT, narc, narc_name)

	old_narc = open(narcfile_path, "wb")
	old_narc.write(narc.save()) 

	print("narc saved")

def write_narc_data(file_name, narc_format, narc, narc_name="trdata"):
	file_path = f'{ROM_NAME}/json/{narc_name}/{file_name}.json'
	narcfile_path = f'{ROM_NAME}/narcs/{narc_name}-{NARC_FILE_ID}.narc'

	stream = bytearray() # bytearray because is mutable

	with open(file_path, "r", encoding='ISO8859-1') as outfile:  	
		json_data = json.load(outfile)	

		#USE THE FORMAT LIST TO PARSE BYTES
		for entry in narc_format: 
			if entry[1] in json_data["raw"]:
				data = json_data["raw"][entry[1]]
				write_bytes(stream, entry[0], data)
	
	if file_name >= len(narc.files):
		narc_entry_data = bytearray()
		narc_entry_data[0:len(stream)] = stream
		narc.files.append(narc_entry_data)
	else:
		narc_entry_data = bytearray(narc.files[file_name])
		narc_entry_data[0:len(stream)] = stream
		narc.files[file_name] = narc_entry_data
	
def write_readable_to_raw(file_name, narc_name="trdata"):
	data = {}
	json_file_path = f'{ROM_NAME}/json/{narc_name}/{file_name}.json'

	with open(json_file_path, "r", encoding='ISO8859-1') as outfile:  	
		json_data = json.load(outfile)	
			
		if json_data["readable"] is None:
			return

		new_raw_data = to_raw(json_data["readable"])
		json_data["raw"] = new_raw_data

	with open(json_file_path, "w", encoding='ISO8859-1') as outfile: 
		json.dump(json_data, outfile)

def to_raw(readable):
	raw = copy.deepcopy(readable)

	raw["class"] = int(readable["class_id"]) 

	

	raw["battle_type"] = BATTLE_TYPES.index(raw["battle_type"])

	for n in range(1, 5):
		raw[f'item_{n}'] = ITEMS.index(raw[f'item_{n}'])


	binary_props = ""
	TEMPLATE_FLAGS.reverse()
	
	for prop in TEMPLATE_FLAGS:
		binary_props += bin(readable[prop])[2:].zfill(1)
	raw["template"] = int(binary_props, 2)

	binary_props = ""
	AIS.reverse()
	
	for prop in AIS:
		binary_props += bin(readable[prop])[2:].zfill(1)
	raw["ais"] = int(binary_props, 2)


	return raw
	

def write_bytes(stream, n, data):
	stream += (int(data).to_bytes(n, 'little'))		
	return stream



################ If run with arguments #############

if len(sys.argv) > 2 and sys.argv[1] == "update":

	file_names = sys.argv[2].split(",")
	 
	for file_name in file_names:
		write_readable_to_raw(int(file_name))
	
# output_narc()

# write_readable_to_raw(1)