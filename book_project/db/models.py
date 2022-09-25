from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class BaseModel(models.Model):
    """
       Abstract base model.
    """
    class Meta:
        abstract = True

    # Save date and time of add and update.
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)



class Book(BaseModel):
    """
       Model for store book.
    """

    class BookCategory(models.TextChoices):
        story = "story", "story"
        educational = "educational", "educational"
        historical = "historical", "historical"

    title = models.CharField(max_length=50)
    category = models.CharField(max_length=15, choices=BookCategory.choices)
    description = models.TextField(null=True)
    author = models.CharField(max_length=15)
    slug = models.SlugField(unique=True, null=True)

    def get_absolute_url(self):
        return reverse("book", kwargs={"slug": self.slug})


class User(BaseModel, AbstractUser):
    """
    Model for store user detail.
    """
    class UserType(models.TextChoices):
        admin = "admin", "admin"
        student = "student", "student"

    username = models.CharField(max_length=75)
    email = models.EmailField(unique=True, max_length=75)
    phone_number = models.BigIntegerField(null=True)
    user_type = models.CharField(choices=UserType.choices, max_length=15)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]


