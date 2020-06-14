from rest_framework import serializers

from main.models import Category, Item


class CategorySerializer(serializers.ModelSerializer):
    """
    Class to serialize Category model to JSON
    Category includes their items (chield elements)
    """

    category_name = serializers.CharField(
        min_length=0,
        max_length=20,
        style={"input_type": "text", "placeholder": "My Category Name"},
    )
    summary = serializers.CharField(
        min_length=2,
        max_length=200,
        style={"input_type": "text", "placeholder": "My category summary"},
    )
    image = serializers.ImageField(required=False)
    category_slug = serializers.CharField(
        style={"input_type": "text", "placeholder": "url-slug-to-category"},
        help_text="Insert the URL slug to redirect to your category. No space allowed!",
    )
    views = serializers.IntegerField(read_only=True)
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


class ItemSerializer(serializers.ModelSerializer):
    """
    Class to serialize Category model to JSON
    Category includes their items (chield elements)
    """

    # Overrides field validation
    # premium_item = serializers.BooleanField(read_only=True)
    # price = serializers.DecimalField(min_value=1.00, max_value=1000000, max_digits=None, decimal_places=2)
    item_name = serializers.CharField(
        min_length=0,
        max_length=20,
        style={"input_type": "text", "placeholder": "My Item Name"},
    )
    summary = serializers.CharField(
        min_length=2,
        max_length=200,
        style={"input_type": "text", "placeholder": "My item summary"},
    )
    content = serializers.CharField(
        min_length=10,
        style={
            "input_type": "text",
            "placeholder": "Write item content here...",
        },
        help_text="To insert formatted text, please use the django administration site.",
    )
    date_published = serializers.DateTimeField(
        help_text="Please use the dropdown menu to select a date and time"
    )
    item_slug = serializers.CharField(
        style={"input_type": "text", "placeholder": "url-slug-to-item"},
        help_text="Insert the URL slug to redirect to your item. No space allowed!",
    )
    views = serializers.IntegerField(read_only=True)

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


class StatSerializer(serializers.Serializer):
    stats = serializers.DictField(child=serializers.IntegerField())
