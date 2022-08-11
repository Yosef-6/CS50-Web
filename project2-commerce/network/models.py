from django.contrib.auth.models import AbstractUser
from django.db import models
from . import util

class User(AbstractUser):
    id        = models.BigAutoField(primary_key=True)
    followers = models.ManyToManyField(to='self',blank=True, symmetrical=False,related_name="Following")#related names are not needed 
    following = models.ManyToManyField(to='self',blank=True, symmetrical=False,related_name="Followers")#but are mandatory for many tomanyfield which are asymetrical
    male      = 'male'
    female    = 'female' 
    human     = 'human'
    identicon = 'identicon'
    bots    = 'bottts'
    avatars ='avataaars'
    jdenticon ='jdenticon'
    gridy     ='gridy'
    micah     ='micah'
    avatarChoices =[
    (male,"male"),
    (female,"female"),
    (human,"human"),
    (identicon,"identicon"),
    (bots,"bottts"),
    (jdenticon,"jdenticon"),
    (avatars,"avataaars"),
    (gridy,"gridy"),
    (micah,"micah"),
    ] 
    avatar    = models.CharField(max_length=15,choices=avatarChoices,default=identicon)
    seed      = models.CharField(max_length=10,blank=True)
    def save(self, *args, **kwargs):
            code = util.get_random_string(10)
            self.seed = code
            super().save(*args, **kwargs)
    #seed is used for Dice bears avatar api 
    def serialize(self):
        return {
            "id"    : self.id,
            "username": self.username,
            "avatar": self.avatar,
            "seed"  : self.seed,
            "followers":[user.username for user in self.followers.all()],
            "following":[user.username for user in self.following.all()],
        }
    def __str__(self):
        return self.username



class Post(models.Model):
    id        = models.BigAutoField(primary_key=True)
    content   = models.TextField(blank=False)
    author    = models.ForeignKey(User,on_delete=models.CASCADE,related_name="authored")
    likes     = models.ManyToManyField(User,related_name="favourites") 
    timestamp = models.DateTimeField(auto_now=True)
    def serialize(self):
        return {
            "id"    : self.id,
            "author": self.author.username,
            "avatar": self.author.avatar,
            "seed"  : self.author.seed,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": [user.username for user in self.likes.all()],
        }
    def __str__(self):
        return f"{self.author}  |  {self.content}  | Likes : {self.likes.count()} | {self.timestamp}"