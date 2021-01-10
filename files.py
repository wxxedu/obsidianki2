#!/usr/bin/env python3

from aqt.utils import showInfo
from aqt import mw
from anki.cards import Card
from anki.notes import Note
from anki.collection import Collection
from . import markdown2
from . import line_processing
from . import obsidian_url
from . import somedata
import datetime

class File:
	
	file_ztk_id = 0
	file_name = ""
	file_content = ""
	file_lines = []
	file_folder_name = ""
	cloze_or_text = ""
	file_obsidian_url  = ""
	first_heading_1 = True
	link_in_metadata = ""
	metadata = []
	tags = []
	
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
		try:
			file_name_segments = self.file_name.split(" ")
			self.file_ztk_id = int(file_name_segments[0])
		except ValueError:
			time = datetime.datetime.now()
			time_str = time.strftime("%y%m%d%H%M%S")
			self.file_ztk_id = int(time_str)
			self.tags.append("ZTK ID Missing")
		return self.file_ztk_id
	
	def get_file_name(self):
		return self.file_name
	
	def get_folder_name(self):
		return self.file_folder_name
	
	def process_file_lines(self):
		code_beginning = False
		for index in range(0, len(self.file_lines)):
			if self.file_lines[index][0] == "`" and self.file_lines[index][1] == "`" and self.file_lines[index][2] == "`":
				code_beginning = not code_beginning
			elif not code_beginning:
				self.file_lines[index] = line_processing.convert(self.file_lines[index])
				if self.file_lines[index][0] == "#" and self.file_lines[index][1] == " " and self.first_heading_1:
					self.first_heading_1 = False
					self.file_lines[index] = self.gen_file_obsidian_url(self.file_lines[index])
					
	
	def get_markdown(self):
		markfile = markdown2.markdown(self.file_content, extras = ["fenced-code-blocks", "metadata", "strike", "tables", "tag-friendly", "task_list", "break-on-newline", "footnotes"])
#		markfile_content = markfile.replace("<h1>", "<h1>" + self.gen_file_obsidian_url() + "[[")
#		markfile_content = markfile_content.replace("</h1>", "]]</a></h1>")
		self.metadata = markfile.metadata
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
		
	def gen_file_obsidian_url(self, line):
		file_name_segements = self.file_name.split(" ")
		obsidian_url_link = obsidian_url.gen_obsidian_url(self.file_ztk_id)
		link_name = ""
		link = "\]\]](" + obsidian_url_link + ")"
		for index in range(1, len(file_name_segements)):
			link_name = link_name + file_name_segements[index]
		
		line_content = ""
		for i in range(2, len(line)):
			if line[i] != "\n":
				line_content = line_content + line[i]
		line_content.rstrip(" ")
		line_content = "# [\[\[" + line_content + link + "\n"
		return line_content
	
	def get_back_extra(self):
		metadata_output = ""
		metadata_count = 0
		for key in self.metadata.keys():
			if key != "tags" and self.metadata[key] != "[]":
				metadata_count = metadata_count + 1
				metadata_output = metadata_output + key + ": " + self.metadata[key] + "≠"
			else:
				tags_string = self.metadata[key].lstrip("[")
				tags_string = tags_string.rstrip("]")
				self.tags = tags_string.split(", ")
		if metadata_count > 0:
			metadata_output = metadata_output.rstrip("≠")
		if metadata_count > 1:
			metadata_output = metadata_output.replace("≠", "<br>")
		return metadata_output
	
	#####################################################################
	#####################################################################
	##                          Write to Anki                          ##
	#####################################################################
	#####################################################################
	
	def write_to_anki(self):
		deck_id = mw.col.decks.id("Obsidian::" + self.file_folder_name)
		mw.col.decks.select(deck_id)
		
		card_model = mw.col.models.byName("Obsidianki")
		
		note_list = mw.col.find_notes(str(self.file_ztk_id))
		find_existing_file = False
		if len(note_list) > 0:
			for single_note_id in note_list:
				single_note = mw.col.getNote(single_note_id)
				if single_note.model() == card_model:
					if single_note["ZTK ID"] == str(self.file_ztk_id):
						single_note["Cloze"] = "{{c1:: }}"
						single_note["Text"] = ""
						single_note[self.cloze_or_text] = self.get_markdown()
						single_note["Back Extra"] = self.get_back_extra()
						for tag in self.tags:
							single_note.addTag(tag)
						card_ids = mw.col.card_ids_of_note(single_note_id)
						mw.col.set_deck(card_ids, deck_id)
						single_note.flush()
						find_existing_file = True 
		if not find_existing_file:
			try:
				deck = mw.col.decks.get(deck_id)
				deck['mid'] = card_model["id"]
				mw.col.decks.save(deck)
				note_object = mw.col.newNote(deck_id)
				note_object["Cloze"] = "{{c1::}}"
				note_object["Text"] = ""
				note_object[self.cloze_or_text] = self.get_markdown()
				note_object["ZTK ID"] = str(self.file_ztk_id)
				note_object["Back Extra"] = self.get_back_extra()
				for tag in self.tags:
					note_object.addTag(tag)
				mw.col.add_note(note_object, deck_id)
			except TypeError:
				if not somedata.no_obsidian_template_info_shown:
					showInfo("<h1>Import Obsidianki Template First!</h1><br>Obsidianki add-on needs the obsidianki template, and you will have to import it for this add-on to work. The Obsidianki template is included in the Obsidianki add-on folder. If you cannot find the add-on folder, please click on <a href = \"https://github.com/wxxedu/obsidianki2/blob/main/Obsidianki.apkg\">this link</a> to download the Obsidianki template.")
					somedata.no_obsidian_template_info_shown = True