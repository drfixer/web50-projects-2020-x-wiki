from random import randrange
from django.shortcuts import render, redirect
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    return render(request, "encyclopedia/entry.html", {

        # added function to turn md into html
        "entry": util.get_entry_html(title),
        "title": title
    })

def search(request):
    query = request.POST['q']
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "entries": util.list_entries()
    })

def new_page(request):
    if request.method == 'POST':
        title = request.POST['title']

        # error if entry alrady exists
        if not util.get_entry(title) == None:
            message = "Entry already exists"
            return render(request, "encyclopedia/error.html", {
                "message": message
            })
        content = request.POST['content']
        f = open(f'entries/{title}.md', 'w')
        f.write(content)
        f.close()
        return redirect(f"/wiki/{title}")
    return render(request, "encyclopedia/new_page.html")

def edit(request, title):
    if request.method == 'POST':
        title = request.POST['title']
        new_content = request.POST['new_content']
        f = open(f'entries/{title}.md', 'w')
        f.write(new_content)
        f.close()
        return redirect(f'/wiki/{title}')
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": util.get_entry(title)
    })

def random(request):
    random_number = randrange(0,len(util.list_entries()))
    entry = util.list_entries()[random_number]
    return redirect(f'/wiki/{entry}')

