import datetime
import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    lastMod = list()
    entryState = list()
    _ , filenames = default_storage.listdir("entries")
    for entries in filenames:
        lastMod.append( (default_storage.get_modified_time(f"entries/{entries}")).strftime("%b %d %Y %H:%M:%S"))
        entryState.append(default_storage.size(f"entries/{entries}"))
    
    return list(sorted(re.sub(r"\.md$", "", filename)  for filename in filenames if filename.endswith(".md"))) , lastMod , entryState
 

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
