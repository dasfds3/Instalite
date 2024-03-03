from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.messages import info
from itertools import chain
from django.contrib.auth.hashers import make_password
from .models import Profile , Post , LikePost , PostCommont
# Create your views here.

@login_required(login_url="core:signin")
def home(request):
    posts = Post.objects.all()
    user = request.user.username
    return render(request, "index.html",{'posts':posts, "user":user})



def signup(request):
    if request.method == "POST":
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]
            password2 = request.POST["password2"]

            if password == password2 and len(str(password)) >= 8 :
                if User.objects.filter(email = email).exists():
                    info(request,"Email Taken")
                    return redirect("core:signup")
                
                elif User.objects.filter(username=username).exists():
                    info(request,"Username Taken")
                    return redirect("core:signup")
                else:
                    user = User.objects.create(username=username,email=email,password=make_password(password))
                    user.save()
                    user_object = User.objects.get(username=username)
                    profile_user = Profile.objects.create(user=user_object,userid=user_object.id)
                    profile_user.save()

                    auth.login(request,user)
                    return redirect("core:setting")
            else:
                info(request,"passwords are not the same")
                return redirect("core:signup")

    else:
        return render(request,"signup.html")



@login_required(login_url="core:signin")
def help(request):
    return render(request,"help.html")


def signin(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("core:setting")
        else: 
            return redirect("core:signin")
        
    else:
        return render(request,"signin.html")

    
@login_required(login_url="splatform:signin")
def setting(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        if request.FILES.get("image") == None:
            user_profile.location = request.POST["location"]
            user_profile.bio = request.POST["bio"]
            user_profile.save()

        elif request.FILES.get("image") != None:
            user_profile.img = request.FILES.get('image')
            user_profile.bio = request.POST["bio"]
            user_profile.location = request.POST["location"]
            user_profile.save()

    return render(request,"setting.html",{"user_profile":user_profile})


def logout(request):
    auth.logout(request)
    return redirect("core:signin")


def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image')
        caption = request.POST['caption']
        new_post = Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')
    

def likepost(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.filter(id = post_id).first()
    
    like_post = LikePost.objects.filter(post_id = post_id, username=username).first()

    if like_post == None:
        new_like = LikePost.objects.create(post_id = post_id, username = username)
        new_like.save()
        post.no_likes = post.no_likes + 1
        post.save()
        return redirect('core:home')
    
    elif like_post != None:
        like_post.delete()
        post.no_likes = post.no_likes - 1 
        post.save()
        return redirect('core:home')
    


    
def profile(request , pk):
    user_object = User.objects.get(username = pk)
    user_profile = Profile.objects.get(user = user_object)


    user_posts = Post.objects.filter(user=pk)
    len_post = len(user_posts)

    context = {
        'user_profile': user_profile,
        'len_post': len_post,
        'user_posts': user_posts,
    }
    return render(request, 'profile.html',context)



def comments(request):
    if request.method == "POST":
        comment = request.POST['comment']
        post_id = request.POST['post_id']
        user = request.user.username

        post = Post.objects.filter(id = post_id).first()

        new_comment = PostCommont.objects.create(user=user, post_id=post_id, content=comment)
        new_comment.save()

        post.comments.set(new_comment)
        post.no_comments = post.no_comments + 1
        post.save()

        posts = Post.objects.all()
        return render(request, "index.html",{'posts':posts})
    else:
        return redirect("core:home")


def deletepost(request):
    post_id = request.GET.get("post_id")
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect("core:home")



def search(request):
    logged_in_user = request.user.username
    user_object = User.objects.get(username=logged_in_user)
    user_profile  = Profile.objects.get(user = user_object)


    if request.method == 'POST':
        username = request.POST["username"] 
        particular_objects = User.objects.filter(username__icontains = username)

        user_object_list = []
        user_profile_list = []

        for user in particular_objects:
            user_object_list.append(user.id)

        for ids in user_object_list:
            user_profilee = Profile.objects.filter(userid = ids)
            user_profile_list.append(user_profilee)
        
        user_profile_list = list(chain(*user_profile_list))
    
    return render(request, "search.html", {"user_profile":user_profile, "user_profile_list":user_profile_list})