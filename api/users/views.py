import json
import logging
from django.utils.translation import gettext_lazy as _
from django.http import Http404
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView

from users.renderers import APIJSONRenderer
from users.models import User
from users.utilities.email import send_email_to_user


from users.serializers import (
    UserRegisterSerializer,
    LoginSerializer,
    UserSerializer,
)


logger = logging.getLogger(__name__)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """
    A view that provides retrieve and update capabilities for a user model.
    To retrieve user data, use GET method, and to update user data, use PUT or PATCH method.

    To retrieve user data:
        - You must be authenticated.
        - Endpoint: users/detail/<int:pk>/

    To update user data:
        - You must be authenticated.
        - Endpoint: users/detail/<int:pk>/
        - Data: {"user": {... updated user data ...}}

    """

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    renderer_classes = (APIJSONRenderer,)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve and return the current authenticated user's data
        """
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        Update and return the current authenticated user's data
        """
        serializer_data = request.data.get('user', {})

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class EmailComfirmationAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    renderer_classes = (APIJSONRenderer,)

    def get(request):
        if request.user is None:
            return Response({'error': 'Invalid user credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        user = json.dumps(request.user)
        return Response(request.user)


class GetActiveUserAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    renderer_classes = (APIJSONRenderer,)

    def get(self, request):
        if request.user is None:
            return Response({'error': 'Invalid user credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = LoginSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [APIJSONRenderer]

    def post(self, request):
        user = request.user
        try:
            # Get the current and new passwords from the request data
            current_password = request.data.get('current_password')
            new_password = request.data.get('new_password')
            # Verify if the current password is correct
            if not user.check_password(current_password):
                return Response({'error': 'Invalid current password'}, status=status.HTTP_400_BAD_REQUEST)

            # Update the user's password with the new password
            user.set_password(new_password)
            user.save()
            #TODO: Make this a background task.  send_email_to_user(user.get('email'))
            serializer = LoginSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), 400)


class ChangeEmailView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [APIJSONRenderer]

    def post(self, request):
        user = request.user
        try:
            # Get the current and new email from the request data
            current_email = request.data.get('current_email')
            new_email = request.data.get('new_email')

            if user.email == new_email:
                return Response({'error': 'Invalid current email and new email are the same'}, status=status.HTTP_400_BAD_REQUEST)

            # Verify if the current email is correct
            if user.email != current_email:
                return Response({'error': 'Invalid current email'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the new email already exists in the system
            if User.objects.filter(email=new_email).exists():
                return Response({'error': 'New email already exists'}, status=status.HTTP_400_BAD_REQUEST)

            # Update the user's email with the new email
            user.email = new_email
            user.save()

            #TODO: Make this a background task.  send_email_to_user(user.get('email'))
            serializer = LoginSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccountAPIView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [APIJSONRenderer]

    def get(self, request):
        user = request.user
        try:
            user.delete()
            #TODO: Make this a background task.  send_email_to_user(user.get('email'))
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            # Handle any exception that occurs during user deletion
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            name = request.data.get('name')

            if name:
                user.display_name = name
                user.save()

            serializer = UserSerializer(user)
            return Response({'msg': 'Updated..', 'data': serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response({'msg': 'Unauthorized change profile', 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class UserLoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    renderer_classes = (APIJSONRenderer,)

    def post(self, request):
        user = {
            "email": request.data.get('email'),
            "password": request.data.get('password')
        }

        try:
            serializer = self.serializer_class(data=user)
            serializer.is_valid(raise_exception=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


class UserRegisterAPIView(generics.CreateAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer
    renderer_classes = (APIJSONRenderer,)

    def post(self, request):
        user = {
            "email": request.data.get('email'),
            "username": request.data.get('email'),
            "password": request.data.get('password'),
            "role": request.data.get('role')
        }
        serializer = self.serializer_class(data=user)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            #TODO: Make this a background task.send_email_to_user(user.get('email'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except TypeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
