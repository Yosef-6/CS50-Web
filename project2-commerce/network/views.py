import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Count
from django.http import  HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Post, User
from django.core.paginator import Paginator


def index(request):
    
    p = Paginator(Post.objects.all().order_by("-timestamp"),10)
    page =  request.GET.get("page",1)
    return render(request, "network/index.html",
                 {
                    "page" : p.page(page)
                 }
    )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email  = request.POST["email"]
        avtar = request.POST["avatar"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password,avatar = avtar)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required(login_url="login")
def manage_post(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body) 
    if(data.get('create_post')):
       Post(author = request.user,content = data.get('post')).save()
    else:
        post = Post.objects.get(pk=data.get('post_id'))
        post.content = data.get('post')
        post.save()
        
    return JsonResponse({"success": "posted successfully"}, status=200)

def fetch_posts(request,user): # fetch post if user=index  ///this function is used to update the index page async when a new post is created
     
            if(user == 'index'):
              posts = Post.objects.all().order_by("-timestamp")
              json_format = [post.serialize() for post in posts]
              p = Paginator(json_format,10) # 10 posts per page
              page =request.GET.get('page',1)
              return JsonResponse(p.page(page).object_list,safe=False)

def fetch_users(request,users):  
   
    if users == "popular"  :
      popularUsers =  User.objects.annotate(Count("followers"))
      json_fromat  = [user.serialize() for user in popularUsers.order_by("-followers__count")[0:5]]
      return JsonResponse(json_fromat,safe=False)
    elif users == "search" :
        searchValue  = request.GET.get('searchValue',"")
        searchUsers  =  User.objects.filter(username__regex=f'{searchValue}')
        json_fromat  =  [user.serialize() for user in searchUsers[0:5]]
        if(searchValue == ''):
            json_fromat = []
        return JsonResponse(json_fromat,safe=False)
    return JsonResponse({"Error": "No such option"}, status=400)

def profile_view(request,id):

    user = User.objects.filter(pk=id).first()
    p = Paginator(Post.objects.all().filter(author=user).order_by("-timestamp"),10)
    page =  request.GET.get("page",1)
    
    return render(request, "network/profile.html",
                 {
                    "userProfile": user,
                    "page" : p.page(page)
                 }
    )
  


              
@csrf_exempt
@login_required(login_url="login")              
def update_post(request,postId):
    try:
        post = Post.objects.get(pk=postId)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if(request.method == "PUT"):
      data = json.loads(request.body)
      if(data.get("like") is not None):
        if(data.get("like") == True):
         post.likes.add(request.user)
        else:
         post.likes.remove(request.user)
        return JsonResponse({"likes": post.likes.count()}, status=200)


@csrf_exempt
@login_required(login_url="login")
def editUserStatus(request,id):
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    if(request.method == "PUT"):
      data = json.loads(request.body)
      if(data.get("follower") is not None):
        if(data.get("follower") == True):
          user.followers.add(request.user)
          request.user.following.add(user)
        else:
          user.followers.remove(request.user)
          request.user.following.remove(user)
         
        return JsonResponse({"followers": user.followers.count()}, status=200)
    
@login_required(login_url="login")
def following_post(request):
    # order the posts of users which the current user follows
    p = Paginator(Post.objects.filter(author__in = [user for user in  request.user.following.all()]).order_by("-timestamp")  ,10)
    page =  request.GET.get("page",1)
    return render(request, "network/following.html",
                 {
                    "page" : p.page(page)
                 }
    )