import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def get_entry_html(title):
    '''Retrieves and encyclopedia entry in html'''
    try:
        return md_to_html(f"entries/{title}.md")
    except FileNotFoundError:
        return None

def file_to_list(md_file):
    '''
    Converts an markdown file to a list of lines in the file as strings
    '''
    f = open(md_file, 'r', encoding="utf-8")
    return f.readlines()

def md_to_html(md_file):
    '''converts an md file to a html in text'''
    converted = file_to_list(md_file)
    converted = header_converter(converted)
    converted = bold_converter(converted)
    converted = list_converter(converted)
    converted = link_converter(converted)
    converted = paragraph_converter(converted)
    converted_final = ""
    for line in converted:
        converted_final += line
    return converted_final

def header_converter(file_list):
    '''
    converts the header in md file to corresponding tags on html'''
    converted = []
    repeats = 0
    for line in file_list:
        if len(re.findall("#+", line)) > 0:
            repeats = len(re.findall("#+", line)[0])
            line += f"</h{repeats}>"
        line = re.sub(f'#{{{repeats}}}', f"<h{repeats}>", line)
        converted.append(line)
    return converted

def bold_converter(file_list):
    '''converts the bold on an md file to the corresponding tag in html'''
    converted = []
    for line in file_list:
        line = re.sub(r"\*\*\b", f"<strong>", line)
        line = re.sub(r"\b\*\*", f"</strong>", line)
        converted.append(line)
    return converted

def list_converter(file_list):
    '''converts list in md to corresponding tags in html'''
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
    '''converts link in md to link tag in html'''
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
    '''converts paragraph in md to corresponding p tag in html'''
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
