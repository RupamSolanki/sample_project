from django.urls import path
from rest_framework.authtoken import views
from user_registration.views import RegistrationView, LogoutView, UserLogoutView, UserRegistrationView, UserLoginView
from rest_framework import routers

router = routers.SimpleRouter()

router.register("rest/register", RegistrationView, basename="user_registration")
urlpatterns = [
    path('restUserLogin/', views.obtain_auth_token),
    path("rest/userLogout/", LogoutView.as_view({"delete": "destroy"}), name="rest_user_logout"),
    path("userRegister/", UserRegistrationView.as_view(), name="user_register"),
    path("userLogin/", UserLoginView.as_view(), name="user_login"),
    path("userLogout/", UserLogoutView.as_view(), name="user_logout"),

]

urlpatterns += router.urls