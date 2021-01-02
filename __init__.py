#!/usr/bin/env python3

from anki import hooks
from aqt import utils
from aqt.utils import showInfo
from aqt.qt import *
from aqt import mw

from .files import File
import os
from . import obsidian_url


vault_path = "/Users/xiuxuan/Library/Mobile Documents/iCloud~org~zrey~metion/Documents/Knowledge Base"


def refresh_obsidian_database():
	showInfo("Database Refreshed")
	files = read_vault()
	obsidian_url.files = files
	for file_object in files:
		file_object.write_to_anki()
	showInfo(str(len(files)))
	
def read_vault():
	files = []
	folders_catalog = os.listdir(vault_path)
	folders_removed = []
	for folder_name in folders_catalog:
		if folder_name[0] == "." or folder_name == "_cover.jpg":
			folders_removed.append(folder_name)
		else:
			folder_path = vault_path + "/" + folder_name
			files_catalog = os.listdir(folder_path)
			for file_name in files_catalog:
				file_name_segments = file_name.split(".")
				if file_name_segments[len(file_name_segments)-1] == "md":
					file_path = folder_path + "/" + file_name
					file_name_no_attribute = ""
					for i in range(0, len(file_name) - 3):
						file_name_no_attribute = file_name_no_attribute + file_name[i]
					with open(file_path, mode = "r", encoding = "utf-8") as f:
						file_object = File(file_name_no_attribute, f.readlines(), folder_name)
						files.append(file_object)
	showInfo("Folders Removed: " + ", ".join(folders_removed))
	return files
	
action = QAction("Import from Obsidian", mw)
action.triggered.connect(refresh_obsidian_database)
mw.form.menuTools.addAction(action)