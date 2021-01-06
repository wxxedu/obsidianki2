#!/usr/bin/env python3

import os
import aqt
import pickle
from aqt.qt import *
from aqt import AnkiQt, gui_hooks
from aqt.utils import tooltip

from PyQt5 import QtWidgets, QtCore


default_settings = {"vault path": "", "wiki-links": False, "italics": True, "highlight": True, "inline code": True, "inline math": True, "display math": False, "bold": False}

SETTINGS_PATH = os.path.expanduser("~/.obsidianki.settings")

def save_settings(settings, path=SETTINGS_PATH):
	with open(path, "wb") as fd:
		pickle.dump(settings, fd)
		
def load_settings(path = SETTINGS_PATH):
	if os.path.isfile(path):
		with open(path, "rb") as fd:
			return pickle.load(fd)
	return default_settings

def get_path_to_vault():
	settings = load_settings()
	return settings["vault path"]

def get_vault_name():
	vault_path = get_path_to_vault()
	vault_path_segments = vault_path.split("/")
	return vault_path_segments[len(vault_path_segments) - 1]

def get_settings_for(syntax):
	settings = load_settings()
	return settings[syntax]

class ObsidiankiSettings(QDialog):
	def __init__(self, mw):
		super().__init__(mw)
		
		layout = QFormLayout(self)
		
		self.vault_path = QLineEdit(self)
		self.wiki_links = QCheckBox(self)
		self.bold = QCheckBox(self)
		self.italics = QCheckBox(self)
		self.highlight = QCheckBox(self)
		self.inline_code = QCheckBox(self)
		self.inline_math = QCheckBox(self)
		self.display_math = QCheckBox(self)
		self.okButton = QPushButton("Okay")
		
		layout.addRow(QLabel("Vault Path: "), self.vault_path)
		layout.addRow(QLabel("Wikilink to Cloze: "), self.wiki_links)
		layout.addRow(QLabel("Bold to Cloze: "), self.bold)
		layout.addRow(QLabel("Italics to Cloze: "), self.italics)
		layout.addRow(QLabel("Highlight to Cloze: "), self.highlight)
		layout.addRow(QLabel("Inline Code to Cloze: "), self.inline_code)
		layout.addRow(QLabel("Inline Math to Cloze: "), self.inline_math)
		layout.addRow(QLabel("Display Math to Cloze"), self.display_math)
		layout.addRow(self.okButton)
		
		settings = load_settings()
		
		try:
			self.vault_path.setText(settings["vault path"])
			self.wiki_links.setChecked(settings["wiki-links"])
			self.bold.setChecked(settings["bold"])
			self.italics.setChecked(settings["italics"])
			self.highlight.setChecked(settings["highlight"])
			self.inline_code.setChecked(settings["inline code"])
			self.inline_math.setChecked(settings["inline math"])
			self.display_math.setChecked(settings["display math"])
		except KeyError:
			self.vault_path.setText(default_settings["vault path"])
			self.wiki_links.setChecked(default_settings["wiki-links"])
			self.bold.setChecked(default_settings["bold"])
			self.italics.setChecked(default_settings["italics"])
			self.highlight.setChecked(default_settings["highlight"])
			self.inline_code.setChecked(default_settings["inline code"])
			self.inline_math.setChecked(default_settings["inline math"])
			self.display_math.setChecked(default_settings["display math"])
			
		self.okButton.clicked.connect(self.onOk)
		
		self.show()
		
	def onOk(self):
		newSettings = {}
		newSettings["vault path"] = self.vault_path.text()
		newSettings["wiki-links"] = self.wiki_links.isChecked()
		newSettings["bold"] = self.bold.isChecked()
		newSettings["italics"] = self.italics.isChecked()
		newSettings["highlight"] = self.highlight.isChecked()
		newSettings["inline code"] = self.inline_code.isChecked()
		newSettings["inline math"] = self.inline_math.isChecked()
		newSettings["display math"] = self.display_math.isChecked()
		save_settings(newSettings)
		self.close()


action = QAction("Obsidianki Settings", aqt.mw)
action.triggered.connect(lambda: ObsidiankiSettings(aqt.mw))

aqt.mw.form.menuTools.addAction(action)