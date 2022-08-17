from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from reviews.models import Title

from .permissions import AuthorOrReadOnly
from .serializers import CommentsSerializer, ReviewsSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    pagination_class = PageNumberPagination
    permission_classes = [AuthorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого отзыва запрещено!')
        super(ReviewViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied('Удаление чужого отзыва запрещено!')
        super(ReviewViewSet, self).perform_destroy(instance)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    pagination_class = PageNumberPagination
    permission_classes = [AuthorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = title.reviews.get(id=self.kwargs.get('review_id'))
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = title.reviews.get(id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого коммента запрещено!')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied('Удаление чужого коммента запрещено!')
        super(CommentViewSet, self).perform_destroy(instance)
