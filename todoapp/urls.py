from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('register/', views.register, name = 'register'),
    path('login/', views.loginpage, name = 'login'),
    path('delete/<str:name>/', views.delete, name = 'delete'),
    path('update/<str:name>/', views.update, name = 'update'),
    path('logout/', views.logoutpage, name = 'logout'),
]