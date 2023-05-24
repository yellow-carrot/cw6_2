from rest_framework import pagination, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import Ad
from ads.permissions import IsStuff, IsOwner
from ads.serializers import AdSerializer

from ads.models import Comment
from ads.serializers import CommentSerializer


class AdPagination(pagination.PageNumberPagination):
    page_size = 3


class AdViewSet(ModelViewSet):
    queryset = Ad.objects.all()
    default_serializer_class = AdSerializer
    pagination_class = AdPagination

    default_permission = [AllowAny]

    permissions = {
        "retrieve": [IsAuthenticated],
        "create": [IsAuthenticated],
        "update": [IsAuthenticated, IsStuff | IsOwner],
        "partial_update": [IsAuthenticated, IsStuff | IsOwner],
        "destroy": [IsAuthenticated, IsStuff | IsOwner]
    }

    serializers = {
        # "create": AdCreateSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        return [permission() for permission in self.permissions.get(self.action, self.default_permission)]

    def list(self, request, *args, **kwargs):
        cat = request.GET.getlist('cat', None)
        if cat:
            self.queryset = self.queryset.filter(category_id__in=cat)

        text = request.GET.get('text', None)
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        location = request.GET.get('location', None)
        if location:
            self.queryset = self.queryset.filter(author_id__location_id__name__icontains=location)

        price_from = request.GET.get('price_from', None)
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)

        price_to = request.GET.get('price_to', None)
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)

        return super().list(request, *args, **kwargs)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
