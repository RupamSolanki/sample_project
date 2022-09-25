from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction, IntegrityError

from book_project.settings import DEFAULT_PAGE_SIZE
from common.constant import constants
from common.form import BookForm
from common.permission import BookPermission
from common.serializer import BookSerializer
from db.models import Book
from django.views.generic import View
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin

class BaseViewMixin(ViewSet):
    """
    Base Mixin class.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, BookPermission]
    lookup_field = '_book'


class BookAPIView(BaseViewMixin):
    """
    Class to manage book, and it includes a methods
    ``create`` to add book,
    ``list`` to fetch book list,
    ``retrieve`` to fetch book detail.
    ``update`` to update book.
    ``partial_update`` to partially update book.
    ``destroy`` to delete book.
    """

    @classmethod
    def _get_query(cls, attr):
        """
        class method of class to generate the model query.
        param attr: A object attribute to create query.
        type attr: str
        """
        return (Q(id=attr)) if attr.isnumeric() else (Q(title=attr) | Q(slug=attr))

    def create(self, request):
        """
        This method includes business logic to add book.
        :param request: A request object consists of query param value.
        :type request: request
        """

        try:
            serializer = BookSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                book = serializer.save()
                return Response({"Data": {"id": book.id},
                                 constants["Message"]: constants["SuccessfullyAdded"].format(
                                     " ".join([book.title, constants["Book"]]))},
                                status=status.HTTP_201_CREATED)
        except ValidationError as err:
            return Response(
                {constants["Error"]: err.args[0],
                 constants["Message"]: constants["ErrorMessage"].format("adding book")},
                status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({constants["Error"]: constants["AlreadyExist"].format(
                " ".join([serializer.validated_data.get('title'), constants["Book"]])),
                constants["Message"]: constants["ErrorMessage"].format("adding book")},
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({constants["Error"]: str(err),
                             constants["Message"]: constants["SomethingWentWrong"].format("adding book")},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """
        This method includes business logic to fetch list of book.
        :param request: A request object consists of query param value.
        :type request: request
        """
        try:
            books = Book.objects.all()
            paginator = PageNumberPagination()
            return Response({"Data": BookSerializer(paginator.paginate_queryset(books, request), many=True).data,
                             constants["Message"]: constants["SuccessfullyFetched"].format(" ".join([
                                 constants["Book"].capitalize(), "list"]))},
                            status=status.HTTP_200_OK)
        except Exception as err:
            return Response({constants["Error"]: str(err),
                             constants["Message"]: constants["SomethingWentWrong"].format("fetching book list")},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, _book):
        """
         This method includes business logic to fetch book detail.
        param request: A request object consists of query param value.
        type request: request
        param _book: A unique value for model object.
        type _book: str
        """
        try:
            return Response({"Data": BookSerializer(Book.objects.get(self._get_query(_book))).data,
                             constants["Message"]: constants["SuccessfullyFetched"].format(constants["Book"])},
                            status=status.HTTP_200_OK)

        except Book.DoesNotExist:
            return Response({constants["Error"]: constants["DoseNotExist"].format(constants["Book"].capitalize()),
                             constants["Message"]: constants["ErrorMessage"].format("fetching book")},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            return Response({constants["Error"]: str(err),
                             constants["Message"]: constants["SomethingWentWrong"].format("fetching book list")},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, _book):
        """
        This method includes business logic to partially update book .
        param request: A request object consists of query param value.
        type request: request
        param _book: A unique value for model object.
        type _book: str
        """
        try:
            serializer = BookSerializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                book = serializer.update(Book.objects.get(self._get_query(_book)), serializer.validated_data)
                return Response({"Data": BookSerializer(book).data,
                                 constants["Message"]: constants["SuccessfullyUpdated"].format(
                                     constants["Book"].capitalize())}, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({constants["Error"]: constants["DoseNotExist"].format(constants["Book"].capitalize()),
                             constants["Message"]: constants["ErrorMessage"].format(constants["UpdatingBook"])},
                            status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({constants["Error"]: constants["AlreadyExist"].format(
                " ".join([serializer.validated_data.get('title'), constants["Book"]])),
                constants["Message"]: constants["ErrorMessage"].format(constants["UpdatingBook"])},
                status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as err:
            return Response({constants["Error"]: err.args[0],
                             constants["Message"]: constants["ErrorMessage"].format(constants["UpdatingBook"])},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({constants["Error"]: str(err),
                             constants["Message"]: constants["SomethingWentWrong"].format(constants["UpdatingBook"])},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, _book):
        """
        This method includes business logic to update book .
        param request: A request object consists of query param value.
        type request: request
        param _book: A unique value for model object.
        type _book: str
        """
        try:
            serializer = BookSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                book = serializer.update(Book.objects.get(self._get_query(_book)), serializer.validated_data)
                return Response({constants["Data"]: BookSerializer(book).data,
                                 constants["Message"]: constants["SuccessfullyUpdated"].format(
                                     constants["Book"].capitalize())}, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({constants["Error"]: constants["DoseNotExist"].format(constants["Book"].capitalize()),
                             constants["Message"]: constants["ErrorMessage"].format(constants["UpdatingBook"])},
                            status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({constants["Error"]: constants["AlreadyExist"].format(
                " ".join([serializer.validated_data.get('title'), constants["Book"]])),
                constants["Message"]: constants["ErrorMessage"].format(constants["UpdatingBook"])},
                status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as err:
            return Response({constants["Error"]: err.args[0],
                             constants["Message"]: constants["ErrorMessage"].format(constants["UpdatingBook"])},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response({constants["Error"]: str(err),
                             constants["Message"]: constants["SomethingWentWrong"].format(constants["UpdatingBook"])},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, _book):
        """
        This method includes business logic to delete book .
        param request: A request object consists of query param value.
        type request: request
        param _book: A unique value for model object.
        type _book: str
        """
        try:
            Book.objects.get(self._get_query(_book)).delete()
            return Response({"Data": {}, constants["Message"]: constants["SuccessfullyDeleted"].format("Book")},
                            status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({constants["Error"]: constants["DoseNotExist"].format(constants["Book"].capitalize()),
                             constants["Message"]: constants["ErrorMessage"].format("deleting book")},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            return Response({constants["Error"]: str(err),
                             constants["Message"]: constants["SomethingWentWrong"].format("deleting book")},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BookView(LoginRequiredMixin, View):
    """
     Class to manage book, and it includes a methods
    ``get`` to display book,
    ``post`` to add book,
    """

    login_url = "/userRegister/"

    @staticmethod
    def get(request, slug=None):
        """
        This method includes business logic to display book list and detail.
        param request: A request object consists of query param value.
        type request: request
        """
        try:
            if slug:
                return render(template_name="book/book_detail.html", request=request,
                              context={"book": Book.objects.get(slug=slug.lower())})
            paginator = Paginator(Book.objects.all(), DEFAULT_PAGE_SIZE)
            context = {"books": paginator.get_page(request.GET.get('page')), "form":  BookForm()}
            return render(template_name="book/book.html", request=request, context=context)
        except Book.DoesNotExist:
            return render(template_name="error.html", request=request)

    @staticmethod
    def post(request):
        """
        This method includes business logic to add book.
        param request: A request object consists of query param value.
        type request: request
        """
        try:
            form = BookForm(request.POST)
            if form.is_valid():
                with transaction.atomic():
                    form.save()
                messages.success(request, 'Book added successfully!')
                return redirect('book_view')
            return render(template_name="error.html", request=request)
        except Exception:
            return render(template_name="error.html", request=request)

# @method_decorator(login_required, name='dispatch')
class BookEditView(LoginRequiredMixin, View):
    """
    Class to manage book, and it includes a methods
    ``get`` to fetch book form,
    ``post`` to update book,
    """

    login_url = "/userRegister/"

    @staticmethod
    def get(request, slug):
        """
        This method includes business logic to display book form.
        param request: A request object consists of query param value.
        type request: request
        """
        try:
            return render(template_name="book/book_detail.html", request=request,
                          context={"form": BookForm(instance=Book.objects.get(slug=slug.lower()))})
        except Book.DoesNotExist:
            return render(template_name="error.html", request=request)

    @staticmethod
    def post(request, slug):
        """
        This method includes business logic to update book.
        param request: A request object consists of query param value.
        type request: request
        """
        try:
            form = BookForm(request.POST, instance=Book.objects.get(slug=slug.lower()))
            if form.is_valid():
                with transaction.atomic():
                    form.save()
                messages.success(request, 'Book updated successfully!')
                return redirect("book_detail", slug=form.instance.slug)
            return render(template_name="error.html", request=request)
        except Exception:
            return render(template_name="error.html", request=request)


# @method_decorator(login_required, name='dispatch')
class BookDeleteView(LoginRequiredMixin, View):
    """
    Class to manage book, and it includes a methods
    ``post`` to delete book,
    """

    login_url = "/userRegister/"

    @staticmethod
    def post(request, slug):
        """
        This method includes business logic to delete book.
        param request: A request object consists of query param value.
        type request: request
        """
        try:
            with transaction.atomic():
                Book.objects.get(slug=slug.lower()).delete()
            messages.success(request, "Book deleted successfully!")
            return redirect("book_view")
        except Exception:
            return render(template_name="error.html", request=request)