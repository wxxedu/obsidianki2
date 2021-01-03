#!/usr/bin/env python3

from anki import hooks
from aqt import utils
from aqt.utils import showInfo
from aqt.qt import *
from aqt import mw

from .files import File
import os
from . import obsidian_url
from . import settings

def refresh_obsidian_database():
	somedata.no_obsidian_template_info_shown = False
	obsidian_url.refresh_obsidian_catalog()
	files = read_vault()
	for file_object in files:
		file_object.write_to_anki()
	
def read_vault():
	files = []
	folders_catalog = os.listdir(settings.path_to_vault)
	for folder_name in folders_catalog:
		if not (folder_name[0] == "." or folder_name == "_cover.jpg" or folder_name.split(".")[len(folder_name.split("."))-1] == ".md"):
			folder_path = settings.path_to_vault + "/" + folder_name
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
	return files
	
action = QAction("Import from Obsidian", mw)
action.triggered.connect(refresh_obsidian_database)
mw.form.menuTools.addAction(action)