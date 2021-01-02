#!/usr/bin/env python3

from aqt.utils import showInfo

vault_root_url = "obsidian://open?vault="
file_root_url = "&file="

files = []

vault_name = "Knowledge Base"

	
def gen_obsidian_url(self, ztk_id):
	vault_url = vault_root_url + encode(vault_name)
	file_url = file_root_url + encode(get_folder_name(ztk_id)) + "%2F" + encode(get_file_name(ztk_id))
	showInfo(vault_url + file_url)
	return vault_url + file_url

def get_folder_name(ztk_id):
	for file_object in files:
		if file_object.get_file_ztk_id() == ztk_id:
			return file_object.get_folder_name()
		
def get_file_name(ztk_id):
	for file_object in files:
		if file_object.get_file_ztk_id() == ztk_id:
			return file_object.get_file_name()

#def remove_file_attribute(file):
#	portions = file.split(".")
#	return_string = ""
#	for index in range(0, len(portions)-1):
#		return_string = return_string + portions[index]
#	return return_string

def encode(string):
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