from django.urls import path, include
from .views import *

urlpatterns = [
    path('create/', UserRegistrationAPI.as_view(), name='create'),
    path('user/<mobile>/', DisplayUserDetailsAPI.as_view(), name='user-details'),
    path('update/', UpdateUserDetailsAPI.as_view(), name='update'),
    path('home/', UserHomePageAPI.as_view(), name='home'),
    # path('login/', UserLoginAPI.as_view(), name='login'),
    # path('logout/', UserLogoutAPI.as_view(), name='logout'),
]
