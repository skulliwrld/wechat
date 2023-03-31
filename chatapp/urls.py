from django.urls import path
from . import views

urlpatterns=[
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('',views.home,name='home'),
    path('logout',views.logout,name='logout'),
    path('<str:room>/',views.room,name='room'),
    path('checkview',views.checkview,name='checkview'),
    path('send',views.send,name='send'),
    path('getMessages/<str:room>/',views.getMessages,name='getMessages')
]