from rest_framework import serializers

from main.models import Category, Item


class ItemSerializer(serializers.ModelSerializer):
    """
    Class to serialize Category model to JSON
    Category includes their items (chield elements)
    """

    # Overrides field validation
    # premium_item = serializers.BooleanField(read_only=True)
    # price = serializers.DecimalField(min_value=1.00, max_value=1000000, max_digits=None, decimal_places=2)
    summary = serializers.CharField(min_length=2, max_length=200)

    class Meta:
        model = Item
        fields = (
            "id",
            "item_name",
            "summary",
            "content",
            "date_published",
            "item_slug",
            "category_name",
            "views",
        )


class CategorySerializer(serializers.ModelSerializer):
    """
    Class to serialize Category model to JSON
    Category includes their items (chield elements)
    """

    summary = serializers.CharField(min_length=2, max_length=200)
    image = serializers.ImageField(required=False)
    child_items = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            "id",
            "category_name",
            "summary",
            "image",
            "category_slug",
            "views",
            "child_items",
        )

    def get_child_items(self, instance):
        """
        SerializerMethod to return a list of serialized model instances
        (many=True)
        """
        items = Item.objects.filter(category_name=instance)
        return ItemSerializer(items, many=True).data

    def to_representation(self, instance):
        return super().to_representation(instance)
