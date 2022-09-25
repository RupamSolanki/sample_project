import random

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from db.models import User, Book
from django.utils.text import slugify
from django.contrib.auth.models import Group, Permission
import faker


@receiver(pre_save, sender=User)
def assign_user_admin(sender, instance, **kwargs):
    """
    This function is created to assign  to the user.
    """

    if instance.user_type == User.UserType.admin:
        instance.is_superuser = True
    return True


@receiver(post_save, sender=User)
def assign_user_to_group(sender, instance, **kwargs):
    """
    This function is created to assign user to the admin.
    """
    if instance.user_type:
        instance.groups.add(Group.objects.get(name=instance.user_type.capitalize()))
    return True


@receiver(pre_save, sender=Book)
def create_book_slug(sender, instance, **kwargs):
    """
    This function is created to store slug in book model.
    """

    instance.slug = slugify(instance.title)
    return True


def populate_groups(sender, **kwargs):
    """
    This method is created to add permission to group.
    """
    groups = Group.objects.all()
    for group in groups:
        if group.name == "Admin":
            query = {}
        else:
            query = {"codename__contains": "view"}
        permissions = Permission.objects.filter(**query)
        group.permissions.add(*permissions)
    return True


def populate_users(sender, **kwargs):
    """
    This method is created to create initial users.
    """
    users = [
        {"email": "admin@mail.com", "first_name": "Admin", "last_name": "Book", "username": "Book Admin",
         "password": "password", "phone_number": "987654321", "user_type": "admin"},
        {"email": "rupam@mail.com", "first_name": "Rupam", "last_name": "Solanki", "username": "Rupam Solanki",
         "password": "password", "phone_number": "987654321", "user_type": "student"},
        {"email": "james@mail.com", "first_name": "James", "last_name": "Woods", "username": "James Woods",
         "password": "password", "phone_number": "987654321", "user_type": "student"},
    ]
    for user in users:
        if not User.objects.filter(email=user["email"]).exists():
            user_inst = User.objects.create(username=user["username"],
                                            first_name=user["first_name"],
                                            last_name=user["last_name"],
                                            email=user["email"],
                                            phone_number=user["phone_number"],
                                            is_staff=True, is_active=True, user_type=user["user_type"],
                                            )
            user_inst.set_password(user["password"])
            user_inst.save()
    return True


def populate_books(sender, **kwargs):
    """
    This method is created to add books.
    """
    fake = faker.Faker()
    category = [category for category in Book.BookCategory]
    if Book.objects.count() <= 25:
        for _ in range(25):
            Book.objects.create(title=fake.company(), category=random.choice(category),
                                description=fake.paragraph(nb_sentences=55), author=fake.name())
    return True
