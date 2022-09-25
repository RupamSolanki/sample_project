from django.urls import path

from book_app.views import BookAPIView, BookView, BookEditView, BookDeleteView
from rest_framework import routers

router = routers.DefaultRouter()

router.register("rest/book", BookAPIView, basename="book")

urlpatterns = [
    path('', BookView.as_view(),name="book_view"),
    path("book/<slug>", BookView.as_view(), name="book_detail"),
    path("bookEdit/<slug>", BookEditView.as_view(), name="book_edit"),
    path("bookDelete/<slug>", BookDeleteView.as_view(), name="book_delete")
]
urlpatterns += router.urls

