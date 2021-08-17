from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name="signup"),
    path('show/', views.show, name="show"),
    path('add_new/', views.add_new, name="add_new"),
    path('insert/', views.insert, name="insert"),
    path('delete/', views.delete, name="delete"),
    path('filter_comment/<str:model>/<str:author>', views.filter_comment, name="filter_comment"),
    path('filter_submission/<str:model>/<str:submission>', views.filter_submission, name="filter_submission")
]   