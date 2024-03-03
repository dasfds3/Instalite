from django.contrib import admin
from .models import Profile , Post , LikePost , PostCommont
# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(PostCommont)