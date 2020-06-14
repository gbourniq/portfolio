from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Category, Item
from .serializers import CategorySerializer, ItemSerializer, StatSerializer
from .services import get_items_by_category_slug


class Pagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class CategoryList(ListAPIView):
    permission_classes = [AllowAny]

    queryset = Category.objects.all()

    # Serializer
    serializer_class = CategorySerializer

    # Filtering
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ("id",)
    search_fields = ("category_name", "summary")

    # Pagination
    pagination_class = Pagination

    def get_queryset(self):
        """
        Override this method to add some custom filtering
        for e.g. based on a boolean field
        """
        return super().get_queryset()


class CategoryCreate(CreateAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        """
        Overrides create method to validate user input,
        E.g: validation of a decimal value
        if request.data.get('price') <= 0.0:
            raise ValidationError({'err_type': 'Must be above £0.00'})
        """
        return super().create(request, *args, **kwargs)


class CategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Category.objects.all()
    lookup_field = "id"
    serializer_class = CategorySerializer

    def delete(self, request, *args, **kwargs):
        """
        Overrides method to update cache
        """
        response = super().delete(request, *args, **kwargs)
        # if response.status_code == status.HTTP_204_NO_CONTENT:
        #     category_id = request.data.get('id')
        #     cache.delete(f'category_data_{category_id}')
        return response

    def update(self, request, *args, **kwargs):
        """
        Overrides method to update cache
        """
        response = super().update(request, *args, **kwargs)
        # if response.status_code == status.HTTP_200_OK:
        #     category = request.data
        #     cache.set(
        #         f'category_data_{category["id"]}',
        #         {
        #             'category_name': category["category_name"],
        #             'summary': category["summary"],
        #             'image': category["image"],
        #             'category_slug': category["category_slug"],
        #         }
        #     )
        return response


class CategoryStats(GenericAPIView):
    """
    GenericAPIView class to generate category stats
    """

    permission_classes = [AllowAny]

    lookup_field = "id"
    serializer_class = StatSerializer
    queryset = Category.objects.all()

    def get(self, request, format=None, id=None):
        """
        returns a stats dictionary response which include
        the total number of items views for the selected category 
        """
        category = self.get_object()
        item_in_category = get_items_by_category_slug(category.category_slug)
        all_views = sum([item.views for item in item_in_category])

        serializer = StatSerializer({"stats": {"all_items_views": all_views,}})
        return Response(serializer.data)


class ItemList(ListAPIView):
    permission_classes = [AllowAny]

    queryset = Item.objects.all()

    # Serializer
    serializer_class = ItemSerializer

    # Filtering
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ("id",)
    search_fields = ("item_name", "summary")

    # Pagination
    pagination_class = Pagination

    def get_queryset(self):
        """
        Override this method to add some custom filtering
        for e.g. based on a boolean field
        """
        return super().get_queryset()


class ItemCreate(CreateAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = ItemSerializer

    def create(self, request, *args, **kwargs):
        """
        Overrides create method to validate user input,
        E.g: validation of a decimal value
        if request.data.get('price') <= 0.0:
            raise ValidationError({'err_type': 'Must be above £0.00'})
        """
        return super().create(request, *args, **kwargs)


class ItemRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Item.objects.all()
    lookup_field = "id"
    serializer_class = ItemSerializer

    def delete(self, request, *args, **kwargs):
        """
        Overrides method to update cache
        """
        response = super().delete(request, *args, **kwargs)
        # if response.status_code == status.HTTP_204_NO_CONTENT:
        #     item_id = request.data.get('id')
        #     cache.delete(f'item_data_{item_id}')
        return response

    def update(self, request, *args, **kwargs):
        """
        Overrides method to update cache
        """
        response = super().update(request, *args, **kwargs)
        # if response.status_code == status.HTTP_200_OK:
        #     item = request.data
        #     cache.set(
        #         f'item_data_{item["id"]}',
        #         {
        #             'item_name': item["item_name"],
        #             'summary': item["summary"],
        #             'content': item["content"],
        #             'summary': item["summary"],
        #             'item_slug': item["item_slug"],
        #             'category_name': item["category_name"],
        #             'views': item["views"],
        #         }
        #     )
        return response
