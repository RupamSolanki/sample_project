# Sample project on Python Using Django and Django rest Framework

# The BookApp

BookApp is a platform where students can read the book online,

BookApp has three built-in users.

- Admin
- Rupam
- James

## Features

- The book app has both server app and rest api.
- Can create, update and delete books.
- Can register users.
- Has both session and token authentication.

# Tech used

- Python 3.10
- Django 4.1.1
- Django Rest Framework 3.13.1
- Mysql
- Bootstrap 5

The book App has two types of users groups **Admin** and **Student**. 
where the Admin users can **create, update and delete** book, And the Student user can **view** book.

Built-in users with their credentials.

- **Admin**
login - Admin@mail.com
password - Password

- **Rupam**
login - Rupam@mail.com
password - Password

- **james**
login - James@mail.com
password - Password

## Installation
Before running the server please update the environment variables in **book_project/book_project.env** file.

install all the packages using below command.

```pip install -r requirments.txt```

Then migrate `python manage.py migrate` and run server `python manage.py runserver`.
