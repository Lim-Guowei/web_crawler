from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name="signup"),
    path('show/', views.show, name="show"),
    path('add_new/', views.add_new, name="add_new"),
    path('insert/', views.insert, name="insert"),
    path('delete/', views.delete, name="delete"),
]   