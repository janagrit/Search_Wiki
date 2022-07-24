import random
from xml.sax.handler import EntityResolver
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import Markdown
from . import util



class NewPage(forms.Form):
    title = forms.CharField(label = "Page Title", widget = forms.TextInput(attrs = {'class': 'form-control col-md-8 col-lg-8'}))
    body = forms.CharField(widget = forms.Textarea(attrs = {'class': 'form-control col-md-8 col-lg-8', 'rows': 10}))



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })



def entryInfo(request, id):
    markdowner = Markdown()
    newpage = util.get_entry(id)
    if newpage is None:
        return render(request, "encyclopedia/notExist.html", {
        "search": id
        })
    convertedPage = markdowner.convert(newpage)
    return render(request, "encyclopedia/entryInfo.html", {
        "title": id,
        "entry": convertedPage
        })



def newPage(request):   
    if request.method == "POST":
        newpage = NewPage(request.POST)
        if newpage.is_valid():
            title = newpage.cleaned_data["title"]
            body = newpage.cleaned_data["body"]
            if util.get_entry(title) == None:
                util.save_entry(title, body)
                return HttpResponseRedirect(reverse("entryInfo", kwargs = {'id': title}))
            else:
                return render(request, "encyclopedia/newPage.html", {
                    "newpage": newpage,
                    "exists": True,
                    "title": title
                })
        else:
            return render(request, "encyclopedia/newPage.html", {
                "newpage": newpage,
                "exists": False,
            })
    else:
        return render(request, "encyclopedia/newPage.html", {
            "pageForm": NewPage(),
            "exists": False
        })

        

def searchEntry(request):
    search = request.GET.get("q", '')
    if(util.get_entry(search) is not None):
        return HttpResponseRedirect(reverse("entryInfo", kwargs={'id': search}))
    else: 
        potentialResults = []
        pages = util.list_entries()
        for page in pages:
            if search.lower() in page.lower():
                potentialResults.append(page)
        
        if len(potentialResults) == 0:
            return render(request, "encyclopedia/notExist.html", {
                "search": search
            })

        return render(request, "encyclopedia/index.html", {
            "search": search,
            "searching": True,
            "entries": potentialResults
        })


def editPage(request, id):
    priviousBody = util.get_entry(id)
    if request.method == "POST":
        newPage = NewPage(request.POST)
        if newPage.is_valid():
            newBody = newPage.cleaned_data["body"]
            util.save_entry(id, newBody)
            return HttpResponseRedirect(reverse("entryInfo", kwargs = {'id': id}))
    else:
        page = NewPage()
        page.fields["title"].initial = id
        page.fields["title"].widget = forms.HiddenInput()
        page.fields["body"].initial = priviousBody
        return render(request, "encyclopedia/editPage.html", {
            "title": id,
            "page": page,
        })


def randomPage(request):
    pages = util.list_entries()
    randomPage = random.choice(pages)
    return HttpResponseRedirect(reverse("entryInfo", kwargs = {'id': randomPage}))



