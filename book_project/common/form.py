from django import forms
from db.models import Book, User
from django.core.exceptions import ValidationError

class BookForm(forms.ModelForm):
    """
    Book form class.
    """
    class Meta:
        model = Book
        fields = ["title", "category", "description", "author"]
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'category': forms.Select(choices=Book.BookCategory, attrs={"class": "form-control"}),
            'description': forms.Textarea(attrs={"class": "form-control"}),
            'author': forms.TextInput(attrs={"class": "form-control"})
        }

class LoginForm(forms.Form):
    """
    Loging form class.
    """
    email = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "off", "required": True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))


class UserRegistrationForm(forms.ModelForm):
    """
    User registration form.
    """
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone_number", "password", "user_type"]

        widgets = {
            "email": forms.TextInput(attrs={"class": "form-control", "autocomplete": "off", "required": True}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "required": False}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "password": forms.PasswordInput(attrs={"class": "form-control", "required": True}),
            "user_type": forms.Select(choices=User.UserType, attrs={"class": "form-control", "required": True}),
        }


