from django.shortcuts import render
from django import forms
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util
import os
from random import choice
from markdown2 import markdown
import re
from datetime import datetime



class NewEntry(forms.Form):
    title = forms.CharField(label="Enter title")
    textarea = forms.CharField(label="Enter your Markdown Text", widget=forms.Textarea(attrs={}))

def escritura_ficheros(path, content):
    """Simple function that writes permanent data."""
    with open(path, "w") as file:
        file.write(content)



def index(request):
    """Function of Index page wiki with list of all .md files."""
    print("DESDE INDEX\n")
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def busqueda(request, busqueda):
    """Function Search and return template with page matched."""
    print("DESDE BUSQUEDA\n")

    meta_url = request.META["PATH_INFO"].split("/")[2:]
    if len(meta_url) > 1:
        title = meta_url[0]
    elif len(meta_url) == 1:
        title = meta_url[0]
    if title != "":
        for item in util.list_entries():
            if title.lower() == item.lower():
                return render(request, "encyclopedia/busqueda.html", {
                    "titulo": item, 
                    "entrada": markdown(util.get_entry(item))
                    })
    return HttpResponseRedirect(reverse("index"))

def new_wiki(request):
    """Function for create to new wiki."""
    print("DESDE      NEW_WIKI   \n")
    if request.method == "POST":
        form = NewEntry(request.POST)        
        if form.is_valid():
            titulo = form.cleaned_data["title"]
            texto = form.cleaned_data["textarea"]

            if titulo not in util.list_entries():
                if "md" in titulo:
                    name = f"{titulo}".replace(".md", "")
                    fichero_md = f"{texto}"
                else:
                    name = titulo
                    fichero_md = f"{texto}"

                ruta_file = f'entries/{name}.md'
                with open(ruta_file, "w") as file:
                    file.write(fichero_md)
                return HttpResponseRedirect(reverse("index"))
            else:
                messages.warning(request, "File already exists!")
        else:
            return render(request, "encyclopedia/new_wiki.html", {
                "formulario": form
                })
    return render(request, "encyclopedia/new_wiki.html", {
        "formulario": NewEntry()
        })

def random_page(request):
    """Function that returns a random page."""
    print("DESDE       RANDOM_PAGE \n")
    file = choice(util.list_entries())
    content = util.get_entry(file)
    to_html = markdown(util.get_entry(file))
    return render(request, "encyclopedia/random.html", {
        "titulo": file,
        "entrada": to_html
        })

def search(request):
    """Function to search for matches in wikis names and returns the clicked wiki page."""
    print("DESDE      SEARCH\n")

    matches = []
    if request.POST["q"] != "":
        for item in util.list_entries():
            if request.POST["q"].lower() in item.lower():
                matches.append(item)
        if len(matches) == 1:
            return render(request, "encyclopedia/busqueda.html", {
                    "titulo": matches[0],
                    "entrada": markdown(util.get_entry(matches[0]))
                    })
        elif len(matches) > 1:
            return render(request, "encyclopedia/search.html", {
                "items": matches
                })
        else:
            return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))


def name_title(request, name_title):
    """Function to Edit Wiki existing."""
    print("DESDE       EDIT\n")
    if request.method == "POST":
        forma = NewEntry(request.POST)        
        if forma.is_valid():
            titulo = forma.cleaned_data["title"]
            texto = forma.cleaned_data["textarea"]
            if "md" in titulo:
                name = f"{titulo}".replace(".md", "")
                fichero_md = f"{texto}"
            else:
                name = titulo
                fichero_md = f"{texto}"

            ruta_file = f'entries/{name}.md'
            with open(ruta_file, "w") as file:
                file.write(fichero_md)
           
            if name != name_title:
                """If the original title is changed and saved, the old file (old .md file) is deleted."""
                os.remove(f"entries/{name_title}.md")
                return HttpResponseRedirect(reverse("busqueda", args=[name]))
            else:
                return HttpResponseRedirect(reverse("busqueda", args=[name_title]))

    forma = NewEntry(initial={"title": name_title, "textarea": util.get_entry(name_title)})
    forma["title"].label = "Edit Title"
    forma["textarea"].label = "Edit Markdown Text"
    return render(request, "encyclopedia/edit.html", {
        "title_file": name_title,
        "formulario_edit": forma,
        })


