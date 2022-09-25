from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from common.form import UserRegistrationForm, LoginForm
from common.serializer import UserRegistrationSerializer
from common.utility import generate_token
from db.models import User
from django.db.utils import IntegrityError
from common.constant import constants
from django.contrib.auth import authenticate, login, logout


class RegistrationView(ViewSet):
    """
    Class to manage user, and it includes a methods
    ``create`` to add user,
    """

    @staticmethod
    def create(request):
        """
        This method includes business logic to add book.
        :param request: A request object consists of query param value.
        :type request: request
        """
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serial_data = serializer.validated_data
                user_inst = User.objects.create(
                    username=" ".join([serial_data.get("first_name"), serial_data.get("last_name")]),
                    first_name=serial_data.get("first_name"),
                    last_name=serial_data.get("last_name"),
                    email=serial_data.get("email"),
                    phone_number=serial_data.get("phone_number"),
                    is_staff=True, is_active=True, user_type=serial_data.get("user_type"))
                user_inst.set_password(serial_data.get("password"))
                user_inst.save()
                token = generate_token(user_inst)
                return Response({constants["Data"]: {"Token": token},
                                 constants["Message"]: constants["SuccessfullyAdded"].format("User")},
                                status=status.HTTP_201_CREATED)
        except ValidationError as err:
            return Response({constants["Error"]: err.args[0],
                             constants["Message"]: constants["ErrorMessage"].format("creating user")},
                            status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({constants["Error"]: constants["AlreadyExist"].format("User"),
                             constants["Message"]: constants["ErrorMessage"].format("creating user")},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({constants["Error"]: str(err),
                             constants["Message"]: constants["SomethingWentWrong"].format("creating user")},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(ViewSet):
    """
    Class to manage user, and it includes a methods
    ``destroy`` to logout user.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def destroy(self, request):
        """
        This method includes business logic to add book.
        param request: A request object consists of query param value.
        type request: request
        """
        try:
            request.user.auth_token.delete()
            return Response({constants["Data"]: "User logged out successfully.",
                             constants["Message"]: "User loggerd out successfully."}, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({constants["Error"]: str(err),
                             constants["Message"]: constants["SomethingWentWrong"].format("creating user")},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserRegistrationView(View):
    """
     Class to manage book, and it includes a methods
    ``post`` to add user,
    """

    @staticmethod
    def get(request):
        """
        This method includes business logic to display user form.
        param request: A request object consists of query param value.
        type request: request
        """
        try:
            if request.user.is_authenticated:
                return redirect('book_view')
            register_form = UserRegistrationForm()
            login_form = LoginForm()
            return render(template_name="user/registration.html", request=request, context={
                "register_form": register_form,
                "login_form": login_form
            })
        except Exception as err:
            return render(template_name="error.html", request=request)

    @staticmethod
    def post(request):
        """
        This method includes business logic to add user.
        param request: A request object consists of query param value.
        type request: request
        """
        try:
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                with transaction.atomic():
                    user_instance = form.save()
                    user_instance.username = " ".join([form.cleaned_data.get("first_name").capitalize(),
                                                       form.cleaned_data.get("last_name").capitalize()])
                    user_instance.set_password(form.cleaned_data.get("password"))
                    user_instance.save()
                    login(request=request, user=user_instance)
                return redirect("book_view")
            messages.warning(request, "Please insert correct value!")
            return redirect("user_register")
        except IntegrityError:
            return render(template_name="error.html", request=request)
        except Exception as err:
            return render(template_name="error.html", request=request)


class UserLogoutView(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        """
        This method includes business logic to logout user.
        param request: A request object consists of query param value.
        type request: request
        """
        login_url = "/userRegister/"

        try:
            logout(request)
            return redirect("user_register")
        except Exception:
            return render(template_name="error.html", request=request)


class UserLoginView(View):
    """
     Class to manage book, and it includes a methods
    ``post`` to login user,
    """

    @staticmethod
    def post(request):
        """
        This method includes business logic to add user.
        param request: A request object consists of query param value.
        type request: request
        """
        try:
            form = LoginForm(request.POST)
            if form.is_valid():
                user_instance = authenticate(request, email=form.cleaned_data.get("email"),
                                             password=form.cleaned_data.get("password"))
                if user_instance:
                    login(request=request, user=user_instance)
                    return redirect("book_view")
            messages.warning(request, "Invalid Credential!")
            return redirect("user_register")
        except IntegrityError:
            return render(template_name="error.html", request=request)
        except Exception as err:
            return render(template_name="error.html", request=request)
