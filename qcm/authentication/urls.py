from django.urls import path
from .views import home,signup,login_view,signout,Configuration,about,ProfileEdit,activate
urlpatterns = [
    path('',home,name='home'),
    path('about/',about,name='about'),
    path('home/',home,name='home'),
    path('signup/',signup,name='signup'),
    path('login/',login_view,name='login'),
    path('signout/',signout,name='signout'),
    path('configure/',Configuration.as_view(),name="configure"),
    path('profile/',ProfileEdit.as_view(),name="profile"),
    path('activate/<uidb64>/<token>',activate,name='activate')
]