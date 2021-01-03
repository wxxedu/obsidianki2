#!/usr/bin/env python3
from . import settings
from . import obsidian_url
from aqt.utils import showInfo 

def convert(line_content):
	line_content = line_content.replace("{{", "{ {")
	line_content = line_content.replace("}}", "} }")
	line_segments = segmentation(line_content)
	line_segments = conversion(line_segments)
	line_segments = wiki_link_processor(line_segments)
	line_content = desegmentation(line_segments)
	return line_content
	
def get_cloze(syntax, begin_or_end):
	cloze = {"begin": "{{c¡::", "end": " }}"}
	syntaxes = settings.whether_to_convert
	if syntaxes[syntax]:
		return cloze[begin_or_end]
	else:
		return ""

def segmentation(line_content):
	line_segments = []
	for i in range(0, len(line_content)):
		line_segments.append(line_content[i])
	return line_segments

def desegmentation(line_segments):
	line_content = ""
	for segment in line_segments:
		line_content = line_content + segment
	return line_content


def conversion(line_segments):
	bold_is_open = True
	highlight_is_open = True
	display_math_is_open = True
	inline_math_is_open = True
	italics_is_open = True
	for i in range(0, len(line_segments) - 1):
		if i < len(line_segments) -1:
			if line_segments[i] == "*" and line_segments[i+1] == "*":
				if bold_is_open:
					line_segments[i] = "**"
					line_segments[i + 1] = get_cloze("bold", "begin")
					bold_is_open = False
				else:
					line_segments[i] = get_cloze("bold", "end")
					line_segments[i + 1] = "**"
					bold_is_open = True
			elif line_segments[i] == "=" and line_segments[i+1] == "=":
				if highlight_is_open:
					line_segments[i] = "<label id = \"highlight\">"
					line_segments[i + 1] = get_cloze("highlight", "begin")
					highlight_is_open = False
				else:
					line_segments[i] = get_cloze("highlight", "end")
					line_segments[i + 1] = "</label>"
					highlight_is_open = True
			elif line_segments[i] == "$" and line_segments[i+1] == "$":
				if display_math_is_open:
					line_segments[i] = "\\\["
					line_segments[i + 1] = get_cloze("display math", "begin")
					display_math_is_open = False
				else:
					line_segments[i] = get_cloze("display math", "end")
					line_segments[i + 1] = "\\\]"
					display_math_is_open = True 
			elif line_segments[i] == "$":
				if inline_math_is_open:
					line_segments[i] = "\\\(" + get_cloze("inline math", "begin")
					inline_math_is_open = False
				else:
					line_segments[i] = get_cloze("inline math", "end") + "\\\)"
					inline_math_is_open = True
			elif line_segments[i] == "*":
				if italics_is_open:
					line_segments[i] = "*" + get_cloze("italics", "begin")
					italics_is_open = False
				else:
					line_segments[i] = get_cloze("italics", "end") + "*"
					italics_is_open = True
		if i == len(line_segments) - 1:
			if line_segments[i] == "$":
				if not inline_math_is_open:
					line_segments[i] = get_cloze("inline math", "end") + "\\\)"
					inline_math_is_open = True
			elif line_segments[i] == "*":
				if not italics_is_open:
					line_segments[i] = get_cloze("italics", "end") + "*"
					italics_is_open = False
	return line_segments

def wiki_link_processor(line_segments):
	anchor_points = []
	has_link = False
	for i in range(0, len(line_segments) - 3):
		if line_segments[i] == "[" and line_segments[i + 1] == "[" and line_segments[i + 2] != "{" and line_segments[i + 3] != "{":
			line_segments[i] = "¶"
			line_segments[i + 1] = "[["
			has_link = True
	for i in range(2, len(line_segments) - 1):
		if line_segments[i] == "]" and line_segments[i + 1] == "]" and line_segments[i - 1] != "}" and line_segments[i - 2] != "}":
			line_segments[i] = "]]"
			line_segments[i + 1] = "¶"
			has_link = True
	if has_link:
		for i in range(0, len(line_segments)):
			if line_segments[i] == "¶":
				anchor_points.append(i)
		for anchor_index in range(0, len(anchor_points) - 1):
			if line_segments[anchor_points[anchor_index] + 1] == "[[":
				wiki_link_content = ""
				needs_split = False 
				for index in range(anchor_points[anchor_index] + 2, anchor_points[anchor_index + 1] - 1):
					check = ""
					wiki_link_content = wiki_link_content + line_segments[index]
					if line_segments[index] == "|":
						needs_split = True
					line_segments[index] = ""
				wiki_link_content_segments_1 = wiki_link_content.split(" ")
				ztk_id = int(wiki_link_content_segments_1[0])
				obsidian_url_link = obsidian_url.gen_obsidian_url(ztk_id)
				wiki_link_name = ""
				if needs_split:
					wiki_link_content_segments_2 = wiki_link_content.split("|")
					wiki_link_name = wiki_link_content_segments_2[len(wiki_link_content_segments_2) - 1]
				else:
					for i in range(1, len(wiki_link_content_segments_1)):
						wiki_link_name = wiki_link_name + wiki_link_content_segments_1[i]
#				obsidian_link = "<a href = \"" + obsidian_url_link + "\">" + wiki_link_name + "</a>"
#				showInfo(wiki_link_name + ": " + obsidian_url_link)
				line_segments[anchor_points[anchor_index]] = "<a href = \"" + obsidian_url_link + "\">"
				line_segments[anchor_points[anchor_index + 1]] = "</a>"
				line_segments[anchor_points[anchor_index] + 2] = wiki_link_name
	return line_segments