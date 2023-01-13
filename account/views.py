
from rest_framework import viewsets
from rest_framework import mixins, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import AuthorRegisterSerializer
from .models import Author, User


class AuthorRegisterAPIView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorRegisterSerializer

    def create_author(self, request, is_author):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save(is_author=is_author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




