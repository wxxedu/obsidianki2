#!/usr/bin/env python3
from . import settings

def convert(line_content):
	line_content = line_content.replace("{{", "{ {")
	line_content = line_content.replace("}}", "} }")
	line_segments = segmentation(line_content)
	line_segments = conversion(line_segments)
	line_content = desegmentation(line_segments)
	return line_content
	
def get_cloze(syntax, begin_or_end):
	cloze = {"begin": "{{c¡::", "end": "}}"}
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
					line_segments[i] == get_cloze("highlight", "end")
					line_segments[i + 1] = "</label>"
					highlight_is_open = True
			elif line_segments[i] == "$" and line_segments[i+1] == "$":
				if display_math_is_open:
					line_segments[i] = "\\["
					line_segments[i + 1] = get_cloze("display math", "begin")
					display_math_is_open = False
				else:
					line_segments[i] = get_cloze("display math", "end")
					line_segments[i + 1] = "\\]"
					display_math_is_open = True 
		if line_segments[i] == "$":
			if inline_math_is_open:
				line_segments[i] = "\\(" + get_cloze("inline math", "begin")
				display_math_is_open = False
			else:
				line_segments[i] = get_cloze("inline math", "end") + "\\)"
		elif line_segments[i] == "*":
			if italics_is_open:
				line_segments[i] = "*" + get_cloze("italics", "begin")
			else:
				line_segments[i] = get_cloze("italics", "end") + "*"
	return line_segments