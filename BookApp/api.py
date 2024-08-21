from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import BookModel
from rest_framework import serializers


class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookModel
        fields = "__all__"

    def validate(self, data):
        price = data["price"]
        if price < 0:
            raise serializers.ValidationError("price cannot be negative")
        return data


# @api_view(["GET"])
# def BookListApi(request):
#     # fetch data from db
#     books = BookModel.objects.all()
#     # convert to json because of the api

#     serializer = BookModelSerializer(books, many=True)

#     return Response(serializer.data)


# # POST request
# @api_view(["POST"])
# def BookCreateApi(request):

#     # get data and post data in the db
#     data = request.data
#     serializer = BookModelSerializer(data=data)

#     if serializer.is_valid():
#         serializer.save()

#     return Response({"message": "Book Created"})


# @api_view(["PUT"])
# def BookUpdateApi(request, id):

#     data = request.data

#     book = BookModel.objects.get(id=id)
#     serializer = BookModelSerializer(instance=book, data=data)

#     if serializer.is_valid():
#         serializer.save()

#         return Response({"message": "updated"})
#     return Response(serializer.errors)


# @api_view(["DELETE"])
# def BookDeleteApi(request, id):
#     book = BookModel.objects.get(id=id)
#     book.delete()

#     return Response({"message": "book deleted"})


from rest_framework.viewsets import ModelViewSet


class BookViewSet(ModelViewSet):
    queryset = BookModel.objects.all()
    serializer_class = BookModelSerializer

    def list(self, request):
        # if not logged in
        if not request.user.is_authenticated:
            return Response({"message": "Please Login"})
        user = request.user
        books = BookModel.objects.filter(author=user)
        serializer = self.get_Serializer(books, many=True)
        return Response(serializer.data)

    def create(self, request):
        # POST
        if not request.user.is_authenticated:
            return Response({"message": "Please Login"})
            # the data is price and name
        data = request.data
        # author
        user = request.user

        serializer = self.get_Serializer(data)

        if serializer.is_valid():
            serializer.save(author=user)
        return Response({"message": "Book Created"})

    def update(self, request, pk):
        # PUT
        if not request.user.is_authenticated:
            return Response({"Please Login"})

        book = BookModel.objects.get(id=pk)
        if book.author == request.user:
            data = request.data
            serializer = self.get_serializer(instance=book, data=data)
            if serializer.is_valid():
                serializer.save()
            return Response({"message": "Book UPdated"})
        return Response({"message": "YOu are not author"})

        data = request.data

    def destroy(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"message": "Please Login"})
        book = BookModel.objects.get(id=pk)
        if book.author == request.user:
            book.delete()
            return Response({"message": "Book Deleted"})
        return Response({"message": "Not authorized to delete the book"})
