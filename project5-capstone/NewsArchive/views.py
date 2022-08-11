import json
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import User,Configuration
from datetime import datetime


def index(request):
    
    return render(request,'NewsArchive/index.html')

def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("dashboard_view"))
        else:
            messages.warning(request,"Invalid username and/or password.")
            return redirect('login')
        
    else:
        return render(request, "NewsArchive/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required(login_url="login")
def dashboard_view(request):
    
    newUser = True 
    request.session["num_visits"]= request.session.get("num_visits",2) + 1
    if(request.session["num_visits"] > 1):
       request.session["num_visits"] = 1
       newUser = False
    return render(request,"NewsArchive/dashboard.html",{
   
      "newUser"       : newUser,
      "configStatus"  : hasattr(request.user,'Settings'),
      "info"          : request.user.Settings.info if hasattr(request.user,'Settings') else 'Config file missing or is not created:create a configuration to aggregate'  

    })

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.info(request,"Passwords must match !!")
            return redirect("register")
        if password == '':
           messages.info(request,"Password field cant be empty")
           return redirect("register")
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request,"Username already taken !!")
            return redirect("register")
            
        
        messages.success(request,"Account created succesfullly login !!")
        request.session["num_visits"] = 0
        return redirect("login")
        
    else:
        return render(request, "NewsArchive/register.html")

@csrf_exempt
@login_required(login_url="login")
def config_save(request):
    if request.method != "POST":
       return JsonResponse({"error": "POST request required."}, status=400)
    
    body = json.loads(request.body)
    config_object = Configuration()   
    if(hasattr(request.user,'Settings')):
        Configuration.objects.filter(config = request.user).first().delete()


    if(body["check"] == "Everthing"):

        config_object.option = Configuration.Everything
        config_object.searchIn = ",".join(body["searchIn"])
        config_object.sources  = ",".join(body["sources_everything"])
        config_object.language = body["language"]
    elif (body["check"] == "Headlines"):
        config_object.option   = Configuration.Topheadlines
        config_object.catagory = body["catagory"]
        config_object.sources  = ",".join(body["sources_headlines"])
        config_object.country  = body["country"]

    config_object.info        = '''Config saved.
                                   Message : your request is qeued for daily content.Be sure to check this info regularly
                                   any config or result related issues are posted here'''
    config_object.queryString = body["queryString"] 
    config_object.config   = request.user
    config_object.active   = True
    config_object.save()     
    return JsonResponse({"Success":"Config saved"},status=200)

@login_required(login_url="login")
def aggregate_info(request):
    info                 = ''    #if there is any issues regarding config
    config_error         = False
    todays_article_count = 0
    if hasattr(request.user,'MyArticles'):
       todays_article_count = request.user.MyArticles.all().filter(aggregatedDate=datetime.now().__str__().split(" ")[0]).count()
      
    if hasattr(request.user,'Settings'):
       if request.user.Settings.active == False:
          info          =  request.user.Settings.info
          config_error  =  True
       else:
          info          =  request.user.Settings.info
    else:
        info ='Config file missing or is not created:create a configuration to aggregate'      
    return JsonResponse({"todays_article_count":todays_article_count,"info":info,"config_error":config_error}, status=200)

@login_required(login_url="login")
def month_info(request,date):
    # date is in format of (year month) only 
    # check if the user has any content and show this by green marker on front end calander
    days=[] #empty no articles were aggregated for that month
    if hasattr(request.user,'MyArticles'):
       month_articles =request.user.MyArticles.all().filter(aggregatedYear=date)
       for articles in month_articles:
            if int(articles.aggregatedDate.split("-")[2]) not in days:
               days.append(int(articles.aggregatedDate.split("-")[2])) # get the date
    return JsonResponse({"days_filled_content":days}, status=200)

@login_required(login_url="login")
def day_data(request,date):
    # date is in format of (year month day) only 
    # fetch articles from database that have been aggregated for the given date
    days_articles=[]
    if hasattr(request.user,'MyArticles'): 
       days_articles = [article.serialize() for article in request.user.MyArticles.all().filter(aggregatedDate=date).order_by("-publishedAt").all()] 
    return JsonResponse({"days_articles":days_articles}, status=200)

@login_required(login_url="login")
def month_data(request,date):
    # date is in format of (year month) only 
    # fetch articles from the database for the user of the month selected
    #empty no articles were aggregated for that month
    month_articles=[]
    if hasattr(request.user,'MyArticles'):
       month_articles = [article.serialize() for article in  request.user.MyArticles.all().filter(aggregatedYear=date).order_by("-publishedAt").all()]
    return JsonResponse({"month_articles":month_articles}, status=200)