#!/usr/bin/env python3

from aqt.utils import showInfo
from .file_content import file_content
from aqt import mw
from anki.cards import Card
from anki.notes import Note
from anki.collection import Collection

class file:
	
	file_ztk_id = 0
	file_name = ""
	file_content_object = file_content([])
	file_folder_name = ""
	
	def __init__(self, file_name, file_content_object, file_folder_name):
		self.file_name = file_name
		self.file_content_object = file_content_object
		self.file_folder_name = file_folder_name
		self.get_file_ztk_id()
	
	def get_file_ztk_id(self):
		file_name_segments = self.file_name.split(" ")
		self.file_ztk_id = int(file_name_segments[0])
		return self.file_ztk_id
	
	def get_file_name(self):
		return self.file_name
	
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
						single_note["Text"] = self.file_content_object.get_text()
						single_note["Back Extra"] = "New Text Extra"
						single_note.flush()
		else:
			note_object = mw.col.newNote(deck_id)
			note_object["Text"] = "Cloze {{c1::trial}}"
			note_object["ZTK ID"] = str(self.file_ztk_id)
			note_object["Back Extra"] = "Text Extra"
			mw.col.add_note(note_object, deck_id)

		return ""