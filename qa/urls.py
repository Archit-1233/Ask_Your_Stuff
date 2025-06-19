from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name='home'),
   path('home/', views.home, name='home'),
    path('upload/', views.upload, name='upload'),
    path('history/', views.history, name='history'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('delete-record/<int:record_id>/', views.delete_record, name='delete_record'),
]