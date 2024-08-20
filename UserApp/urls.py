from django.urls import path
from .api import *

urlpatterns = [
    path("create", UserCreateApi),
    # path("login", UserLoginApi),
    path("protected", ProtectedView),
]
