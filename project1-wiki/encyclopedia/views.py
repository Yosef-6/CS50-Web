from django.http import HttpResponse
from django.shortcuts import render
import markdown2,random
from . import util,forms

def index(request):
    
    name = request.GET.get('q','')
    entries,lastMod,entryState = util.list_entries()
    
    if name == '' :
      return render(request, "encyclopedia/index.html", {
        "info": zip(entries,lastMod,entryState),
        "searchInfo":"All Pages"
        })
    elif util.get_entry(name) is not None:
        return entryView(request,name)
    else:
        matchedEntries = list()
        matchedLastMod = list()
        matchedEntryState = list() 
        for e in entries:
            if name in e:
                matchedEntries.append(e)
                matchedLastMod.append(lastMod[entries.index(e)])
                matchedEntryState.append(entryState[entries.index(e)])
    if len(matchedEntries) != 0:
            return render(request, "encyclopedia/index.html", {
            "info": zip(matchedEntries,matchedLastMod,matchedEntryState),
            "searchInfo":f"Search Results for '{name}'"
        })
    else :
            return entryView(request,name)
  
def randomView(request):
    
    entries,_,__ = util.list_entries()
    return entryView(request,random.choice(entries))  

def newEntry(request):
    if request.method == 'GET': 
        form =  forms.EntryForm()
        return render (request,"encyclopedia/newEntry.html",{
              "title" : "Create New Entry",
              "form"  :  form,
              "Error"  :   -1
        })
    else:
        form = forms.EntryForm(request.POST)
        if(form.is_valid()):
           if util.get_entry(form.cleaned_data["title"]) is None:
              util.save_entry(form.cleaned_data["title"],form.cleaned_data["description"])
              return entryView(request,form.cleaned_data["title"])
 
           else:
               return render (request,"encyclopedia/newEntry.html",{
              "title" : "Create New Entry",
              "form"  :   form,
              "Error"  :    1
        })

              

def existEntry(request,name):
    
   
    if request.method == 'GET':
        if util.get_entry(name) is not None:
         form =  forms.EntryForm()
         form.fields["title"].initial = name
         form.fields["title"].help_text ="Entry name must not be changed"
         form.fields["description"].initial = util.get_entry(name)
         return render (request,"encyclopedia/existEntry.html",{
              "title" : f"Edit '{name}' Entry Exist !!",
              "form"  :  form,
              "Error" :   0
        })
        else:
            return index(request)
    else:
        form = forms.EntryForm(request.POST)
        
        if (form.is_valid()) :
            if form.cleaned_data["title"] == name:
               util.save_entry(form.cleaned_data["title"],form.cleaned_data["description"])
               return entryView(request,form.cleaned_data["title"])
            else:
               return render (request,"encyclopedia/existEntry.html",{
              "title" : f"Edit '{name}' Entry Exist !!",
              "form"  :  form,
              "Error" :    1
        })

        else:
            return randomView(request)

    

def entryView(request,name = None):
    
    
        if util.get_entry(name) is None:
            return render(request,"encyclopedia/entries.html",{
                 
                  "title": "Page not found",
                  "info" : f"<h1 class='display-4'>The requested page '{name}' was not found </h1>" 
             })
        else:

         return render(request,"encyclopedia/entries.html",{
                  
                  "title": name,
                  "info" : markdown2.markdown(util.get_entry(name)),
                  "editable": 1 
         })

    





          

  
