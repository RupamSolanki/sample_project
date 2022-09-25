from rest_framework import serializers
from db.models import User, Book


class UserRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=25)
    last_name = serializers.CharField(max_length=25)
    user_type = serializers.ChoiceField(choices=User.UserType)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "phone_number", "user_type"]


class BookSerializer(serializers.ModelSerializer):
    category = serializers.ChoiceField(choices=Book.BookCategory, error_messages={
        "invalid_choice": "Invalid category. Valid Categories are `story`, `educational`, `historical`."})

    class Meta:
        model = Book
        fields = ["id", "title", "category", "description", "author", "slug"]
