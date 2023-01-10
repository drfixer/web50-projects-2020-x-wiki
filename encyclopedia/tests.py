from django.test import TestCase
import re

# Create your tests here.

def file_to_list(md_file):
    f = open(md_file, 'r', encoding="utf-8")
    return f.readlines()

def md_to_html(md_file):
    converted = file_to_list(md_file)
    #converted = header_converter(converted)
    #converted = bold_converter(converted)
    converted = list_converter(converted)
    #converted = link_converter(converted)
    converted = paragraph_converter(converted)
    converted_final = ""
    for line in converted:
        converted_final += line
    return converted_final

def header_converter(file_list):
    converted = []
    for line in file_list:
        if len(re.findall("#+", line)) > 0:
            repeats = len(re.findall("#+", line)[0])
            line += f"</h{repeats}>"
        line = re.sub(f'#{{{repeats}}}', f"<h{repeats}>", line)
        converted.append(line)
    return converted

def bold_converter(file_list):
    converted = []
    for line in file_list:
        line = re.sub(r"\*\*\b", f"<strong>", line)
        line = re.sub(r"\b\*\*", f"</strong>", line)
        converted.append(line)
    return converted

def list_converter(file_list):
    converted = []
    unordered = False
    for line in file_list:
        if len(re.findall("\*", line)) > 0:
            if unordered == False:
                line = "<ul>" + line
                unordered = True
            line = re.sub("\*", "<li>", line)
            line += "</li>"
        else:
            if unordered:
                converted[len(converted) - 1] += "</ul>"
                unordered = False
        converted.append(line)
    return converted

def link_converter(file_list):
    converted = []
    for line in file_list:
        matches = re.findall("\[[^\[]*\)", line)
        for match in matches:
            title = re.findall("(?<=\[).*(?=\])", match)[0]
            link = re.findall("(?<=\().*(?=\))", match)[0]
            a_format = f"<a href='{link}'>{title}</a>"
            line = re.sub(re.escape(match), a_format, line)
        converted.append(line)
    return converted

def paragraph_converter(file_list):
    converted = []
    first_blank = True
    for line in file_list:
        if len(line) <= 1:
            if first_blank == True:
                line += "<p>"
                first_blank = False
            else:
                line += "</p><p>"
        converted.append(line)
    converted.append("</p>")
    return converted

print(md_to_html("/Users/josej.echenique/Desktop/virtual-env/wiki/entries/HTML.md"))