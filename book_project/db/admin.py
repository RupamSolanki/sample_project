from django.contrib import admin
from db.models import User, Book


@admin.register(User)
class AppUserAdmin(admin.ModelAdmin):
    """
     Class to manage user table on admin panel.
    """
    filter_horizontal = ("groups", "user_permissions")
    list_display = ["email"]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Class to manage user table on book panel.
   """
    list_display = ["title", "created", "updated"]