from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("",views.home, name="home"),
    path("signup/",views.signup,name="signup"),
    path("help/",views.help,name="help"),
    path("signin/",views.signin,name="signin"),
    path("setting/", views.setting, name="setting"),
    path("logout/",views.logout,name="logout"),
    path('upload/',views.upload,name="upload"),
    path('likepost/',views.likepost,name='likepost'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path("comments/",views.comments, name="comment"),
    path("deletepost/", views.deletepost, name="delete"),
    path("search/",views.search, name="search")
]
