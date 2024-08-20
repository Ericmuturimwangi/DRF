from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser


@api_view(["POST"])
def UserCreateApi(request):

    username = request.data["username"]
    password = request.data["password"]

    User.objects.create_user(username=username, password=password)

    return Response({"message": "User created"})


# @api_view(["POST"])
# def UserLoginApi(request):
#     # Extract username and password from request data
#     username = request.data.get("username")
#     password = request.data.get("password")

#     if not username or not password:
#         return Response(
#             {"message": "Username and password are required"},
#             status=status.HTTP_400_BAD_REQUEST,
#         )

#     # Manually create a Django HttpRequest object if needed for testing
#     # or simply use the data to authenticate
#     user = authenticate(username=username, password=password)

#     if user is not None:
#         login(request, user)  # Login method should be called with the request object
#         token, created = Token.objects.get_or_create(user=user)
#         return Response(
#             {"message": "User Logged In", "token": token.key}, status=status.HTTP_200_OK
#         )
#     else:
#         return Response(
#             {"message": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
#         )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def ProtectedView(request):
    return Response(
        {"message": "This is a protected view", "username": request.user.username}
    )
