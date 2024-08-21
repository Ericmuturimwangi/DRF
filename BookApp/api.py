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
