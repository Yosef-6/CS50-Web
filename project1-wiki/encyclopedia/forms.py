from turtle import title
from unicodedata import name
from django import forms



class EntryForm(forms.Form):

    
      title = forms.CharField(label="Title :", widget=forms.TextInput(attrs={"placeholder":"Enter Title :" , "id":"Title" ,"class":"form-control",})) 
      description = forms.CharField(required="",label="Content :" , widget=forms.Textarea(attrs={
                                
                                "class":"form-control",
                                "id":"Discription",
                                "placeholder":"Enter Content using MD :",
                                "style":"height:200px",
                               
                
                   }))
           