from django.urls import path, include
from .views import *

urlpatterns = [
    path('create-user/', OpenAccountView.as_view(), name='create-user'),
    path('user/<mobile>/', DisplayUserDetailsAPI.as_view(), name='user-details'),
]
