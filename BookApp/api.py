from rest_framework import serializers
from .models import BookModel
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import BookModel
from rest_framework.pagination import PageNumberPagination


class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookModel
        fields = "__all__"

    def validate(self, data):
        price = data.get("price")
        if price < 0:
            raise serializers.ValidationError("Price cannot be negative")
        return data


class BookViewSet(ModelViewSet):
    queryset = BookModel.objects.all()
    serializer_class = BookModelSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination

    def list(self, request):
        user = request.user
        books = (
            BookModel.objects.filter(author=user)
            if user.is_authenticated
            else BookModel.objects.none()
        )
        page = self.paginate_queryset(books)
        serializer = self.get_serializer(books, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=user)
            return Response({"message": "Book Created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response(
                {"message": "Please Login"}, status=status.HTTP_401_UNAUTHORIZED
            )

        book = get_object_or_404(BookModel, pk=pk)
        if book.author == request.user:
            serializer = self.get_serializer(book, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Book Updated"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"message": "You are not the author"}, status=status.HTTP_403_FORBIDDEN
        )

    def destroy(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response(
                {"message": "Please Login"}, status=status.HTTP_401_UNAUTHORIZED
            )

        book = get_object_or_404(BookModel, pk=pk)
        if book.author == request.user:
            book.delete()
            return Response(
                {"message": "Book Deleted"}, status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {"message": "Not authorized to delete this book"},
            status=status.HTTP_403_FORBIDDEN,
        )
