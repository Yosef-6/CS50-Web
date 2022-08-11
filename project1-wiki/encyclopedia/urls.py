from importlib.metadata import EntryPoint
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("random/",views.randomView,name="random"),
    path("editEntry/newEntry",views.newEntry,name="newEntry"),
    path("editEntry/existEntry/<str:name>",views.existEntry,name="existEntry"),
    path("<str:name>/",views.entryView,name="entryView"),
]

