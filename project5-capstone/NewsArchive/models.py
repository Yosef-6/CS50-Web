import string
from turtle import title
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Configuration(models.Model):
    id     = models.BigAutoField(primary_key=True)
    Everything = 'Everything'
    Topheadlines = 'Topheadlines' 
    optionChoices =[
    (Everything,"Everything"),
    (Topheadlines,"Topheadlines"),
    ]
    option       = models.CharField(max_length=15,blank=False,choices=optionChoices,default=Everything)
    queryString  = models.CharField(max_length=20,blank=True)
    searchIn     = models.TextField(blank=True)
    sources      = models.TextField(blank=True)
    language     = models.CharField(max_length=10,blank=True)
    catagory     = models.CharField(max_length=30,blank=True)
    country      = models.CharField(max_length=20,blank=True)
    info         = models.TextField(blank=True)
    active       = models.BooleanField(auto_created=False)
    config_date  = models.DateField(auto_now=True)
    config       = models.OneToOneField(to=User,on_delete=models.CASCADE,related_name="Settings")
    def __str__(self):
        return self.config.username + " Config"
    

class Article(models.Model):
    id                = models.BigAutoField(primary_key=True)
    author            = models.CharField(max_length=20,blank=False)
    title             = models.TextField(blank=False,null=True)
    discription       = models.TextField(blank=False,null=True)
    article_url       = models.URLField(blank=True,max_length=450,null=True)
    article_image_url = models.URLField(blank=True,max_length=450,null=True)
    publishedAt       = models.DateTimeField(auto_created=True)
    aggregatedDate    = models.CharField(max_length=20,blank=False,null=True)
    aggregatedYear    = models.CharField(max_length=20,blank=True,null=True) #is used to easily filter the articles for month data to improve performance
    content           = models.TextField(blank=False,null=True)
    viewer            = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name="MyArticles")
    
    def save(self, *args, **kwargs):
        date = self.aggregatedDate.split("-")[0:2]
        date[1] = f'{int(date[1])}'
        self.aggregatedYear =" ".join(date)
        self.title              ="No title" if self.title == '' else  self.title
        self.discription        ="No description" if self.discription  == '' else  self.discription 
        self.article_image_url  ="https://previews.123rf.com/images/infadel/infadel1712/infadel171200119/91684826-a-black-linear-photo-camera-logo-like-no-image-available-.jpg" if self.article_image_url  == '' else  self.article_image_url 
        self.article_url        ="https://previews.123rf.com/images/infadel/infadel1712/infadel171200119/91684826-a-black-linear-photo-camera-logo-like-no-image-available-.jpg" if self.article_url  == '' else  self.article_url
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def serialize(self):
        return {
            "author": self.author,
            "title": self.title,
            "discription":self.discription,
            "article_url": self.article_url,
            "article_image_url": self.article_image_url,
            "publishedAt": self.publishedAt.strftime("%b %d %Y, %I:%M %p"),
            "content": self.content,
        }