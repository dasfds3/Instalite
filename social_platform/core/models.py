from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    userid = models.IntegerField()
    bio = models.TextField(blank=True)
    img = models.ImageField(upload_to="user_pics",default="default.jpg")
    email = models.EmailField()
    location = models.CharField(max_length=100,blank=True)
    follower = models.IntegerField(default = 0)
    following = models.IntegerField(default = 0)

    def __str__(self) -> str:
        return self.user.username
    

class Post(models.Model):
    user = models.CharField(max_length= 50)
    post_id = models.UUIDField(default=uuid.uuid4)
    caption = models.TextField()
    comments = models.ManyToManyField("PostCommont",related_name="posts", null=True,blank=True)
    no_comments = models.IntegerField(default=0)
    image = models.ImageField(upload_to="post_pics")
    date_time = models.DateTimeField(default=timezone.now)
    no_likes = models.IntegerField(default=0)


    def __str__(self) -> str:
        return self.user
    

class LikePost(models.Model):
    post_id = models.CharField(max_length=90)
    username = models.CharField(max_length= 60)



class PostCommont(models.Model):
    content = models.TextField()
    date_time = models.DateTimeField(default=timezone.now)
    user = models.CharField(max_length=80)
    post_id = models.CharField(max_length=150)

