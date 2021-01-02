#!/usr/bin/env python3

from aqt.utils import showInfo
from aqt import mw
from anki.cards import Card
from anki.notes import Note
from anki.collection import Collection
from . import markdown2
from . import line_processing

class File:
	
	file_ztk_id = 0
	file_name = ""
	file_content = ""
	file_lines = []
	file_folder_name = ""
	cloze_or_text = ""
	
	def __init__(self, file_name, file_lines, file_folder_name):
		self.file_name = file_name
		self.file_lines = file_lines
		has_empty_lines = False
		for line in self.file_lines:
			if line == "\n":
				has_empty_lines = True
		if has_empty_lines:
			self.file_lines.remove("\n")
		self.file_folder_name = file_folder_name
		self.get_file_ztk_id()
		self.process_file_lines()
		self.get_file_content()
		self.cloze_or_text = self.get_cloze_or_text()
		
	
	def get_file_ztk_id(self):
		file_name_segments = self.file_name.split(" ")
		self.file_ztk_id = int(file_name_segments[0])
		return self.file_ztk_id
	
	def get_file_name(self):
		return self.file_name
	
	def get_folder_name(self):
		return self.file_folder_name
	
	def process_file_lines(self):
		for index in range(0, len(self.file_lines)):
			self.file_lines[index] = line_processing.convert(self.file_lines[index])
	
	def get_markdown(self):
		markfile = markdown2.markdown(self.file_content, extras = ["fenced-code-blocks", "metadata", "strike", "tables", "tag-friendly", "task_list", "break-on-newline"])
		return markfile
	
	def get_file_content(self):
		self.file_content = "".join(self.file_lines)
	
	def get_cloze_or_text(self):
		if self.file_content.find("¡") > -1:
			count = 0
			while self.file_content.find("¡") > -1:
				count = count + 1
				self.file_content = self.file_content.replace("¡", "%d"%(count), 1)
			return "Cloze"
		else:
			return "Text"	
	####################################################################
	####################################################################
	## 						Write to Anki							  ##
	####################################################################
	####################################################################
	
	def write_to_anki(self):
		deck_id = mw.col.decks.id(self.file_folder_name)
		mw.col.decks.select(deck_id)
		
		card_model = mw.col.models.byName("Obsidianki")
		
		note_list = mw.col.find_notes(str(self.file_ztk_id))
		if len(note_list) > 0:
			for single_note_id in note_list:
				single_note = mw.col.getNote(single_note_id)
				if single_note.model() == card_model:
					if single_note["ZTK ID"] == str(self.file_ztk_id):
						single_note["Cloze"] = "{{c1:: }}"
						single_note["Text"] = ""
						single_note[self.cloze_or_text] = self.get_markdown()
						single_note["Back Extra"] = ""
						single_note.flush()
		else:
			note_object = mw.col.newNote(deck_id)
			note_object[self.cloze_or_text] = self.get_markdown()
			note_object["ZTK ID"] = str(self.file_ztk_id)
			note_object["Back Extra"] = ""
			mw.col.add_note(note_object, deck_id)