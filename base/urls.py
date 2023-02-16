from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (TokenRefreshView)

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view()),
    path('singup/', views.register),
    path('profile/', views.crudView.as_view()),
    path('post/', views.postcrudView.as_view()),
    path('delete/<id>', views.postcrudView.as_view()),
    path('edit/<id>', views.postcrudView.as_view()),
    path('token/refresh/',TokenRefreshView.as_view())

]
