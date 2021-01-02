#!/usr/bin/env python3

from aqt.utils import showInfo
from .file_content import file_content

class file:
	
	file_ztk_id = 0
	file_name = ""
	file_content_object = file_content([])
	file_folder_name = ""
	
	def __init__(self, file_name, file_content_object, file_folder_name):
		self.file_name = file_name
		self.file_content_object = file_content_object
		self.file_folder_name = file_folder_name
	
	def get_file_ztk_id(self):
		file_name_segments = self.file_name.split(" ")
		self.file_ztk_id = int(file_name_segments[0])
		return self.file_ztk_id
	
	def add_to_anki(self):
		
		return self.file_content