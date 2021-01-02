#!/usr/bin/env python3

from anki import hooks
from aqt import utils
from aqt.utils import showInfo
from aqt.qt import *
from aqt import mw

from .file import file
from .file_content import file_content

def refresh_obsidian_database():
	showInfo("Database Refreshed")
	
	
action = QAction("Import from Obsidian", mw)
action.triggered.connect(refresh_obsidian_database)
mw.form.menuTools.addAction(action)