from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import News, NewsStatus, Status, Comment
from .serializers import NewsSerializer, StatusNewsSerializer, CommentSerializer
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from .permissions import PostPermission
from rest_framework import permissions


class PostPagePagination(PageNumberPagination):
    page_size = 3


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [PostPermission, ]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['text', ]
    search_fields = ['text', ]
    ordering_fields = ['created_at']
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.profile)

    @action(methods=['POST'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def leave_status(self, request, pk=None):
        serializer = StatusNewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                profile=request.user.profile,
                news=self.get_object()
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [PostPermission, ]

    def get_queryset(self):
        return super().get_queryset().filter(tweet_id=self.kwargs.get('news_id'))

    def perform_create(self, serializer):
        serializer.save(
            profile=self.request.user.profile,
            news_id=self.kwargs.get('news_id')
        )

