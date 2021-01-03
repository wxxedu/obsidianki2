#!/usr/bin/env python3

from aqt.utils import showInfo
from . import settings
import os 

vault_root_url = "obsidian://open?vault="
file_root_url = "&file="
vault_name = settings.vault_name

folders = {}
files = {}
folders_catalog = os.listdir(settings.path_to_vault)
folders_removed = []

def refresh_obsidian_catalog():
	for folder_name in folders_catalog:
		if not (folder_name[0] == "." or folder_name == "_cover.jpg" or folder_name.split(".")[len(folder_name.split("."))-1] == "md"):
			folder_path = settings.path_to_vault + "/" + folder_name
			files_catalog = os.listdir(folder_path)
			for file_name in files_catalog:
				file_name_segments_1 = file_name.split(".")
				if file_name_segments_1[len(file_name_segments_1)-1] == "md":
					file_name_segments_2 = file_name.split(" ")
					ztk_id = int(file_name_segments_2[0])
					folders[ztk_id] = folder_name
					file_name_segments_3 = []
					for index in range(0, len(file_name_segments_1) - 1):
						file_name_segments_3.append(file_name_segments_1[index])
					file_name = " ".join(file_name_segments_3)
					files[ztk_id] = file_name
	
def gen_obsidian_url(ztk_id):
	vault_url = vault_root_url + my_encode(vault_name)
	file_url = file_root_url + my_encode(get_folder_name(ztk_id)) + my_encode(get_file_name(ztk_id))
	return vault_url + file_url
	

def get_folder_name(ztk_id):
	try:
		return folders[ztk_id] + "%2F"
	except KeyError:
		return ""
			
def get_file_name(ztk_id):
	try: 
		keychain = ""
		return files[ztk_id]
	except KeyError:
		return ""
	
	
#def remove_file_attribute(file):
#	portions = file.split(".")
#	return_string = ""
#	for index in range(0, len(portions)-1):
#		return_string = return_string + portions[index]
#	return return_string

def my_encode(string):
	string = str(str(string).encode("utf-8"))
	string = string.replace("\\x", "%")
	string = string.replace(" ", "%20")
	string = string.replace("/", "%2F")
	string = string.lstrip("\'b")
	string = string.rstrip("\'")
	string = capitalize_unicode(string)
	return string

def capitalize_unicode(string):
	new = []
	position = -5
	for index in range(0, len(string)):
		if string[index] == "%":
			position = index
			new.append(string[index])
		elif index == position + 1 or index == position + 2:
			new.append(string[index].capitalize())
		else:
			new.append(string[index])
	return "".join(new)