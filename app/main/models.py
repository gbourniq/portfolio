import logging
import sys
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.utils import timezone
from PIL import Image

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)

# Global variables
UPLOADS_FOLDER_PATH = "images/"
THUMBNAIL_SIZE = (500, 500)
CROP_SIZE = (300, 300)


def resizeImage(uploadedImage: ImageFieldFile) -> ImageFieldFile:
    """
    Performs the following operation on a given image:
    - Thumbmail: returns an image that fits inside of a given size (preserving aspect ratios)
    - Crop: Cut image borders to fit a given size
    """
    # Load
    img_temp = Image.open(uploadedImage)
    outputIoStream = BytesIO()

    # Preprocess
    img_temp.thumbnail(THUMBNAIL_SIZE)
    width, height = img_temp.size
    left = (width - CROP_SIZE[0]) / 2
    top = (height - CROP_SIZE[1]) / 2
    right = (width + CROP_SIZE[0]) / 2
    bottom = (height + CROP_SIZE[1]) / 2
    img_temp = img_temp.crop((left, top, right, bottom))

    # Save
    img_temp.save(outputIoStream, format="JPEG", quality=90)
    outputIoStream.seek(0)
    uploadedImage = InMemoryUploadedFile(
        outputIoStream,
        "ImageField",
        "%s.jpg" % uploadedImage.name.split(".")[0],
        "image/jpeg",
        sys.getsizeof(outputIoStream),
        None,
    )
    return uploadedImage


# Create your models here.\
class Category(models.Model):
    category_name = models.CharField(max_length=200, unique=True)
    summary = models.TextField()
    image = models.ImageField(upload_to=UPLOADS_FOLDER_PATH)
    category_slug = models.CharField(max_length=200, unique=True)

    @classmethod
    def create(cls, dictionary):
        """
        Class method to instantiate a Category objects with dictionaries.
        """
        return cls(**dictionary)

    def json(self):
        """
        Returns class attributes as a dictionary.
        """
        return {
            "category_name": self.category_name,
            "summary": self.summary,
            "image": self.image,
            "category_slug": self.category_slug,
        }

    def save(self, *args, **kwargs):
        # if not self.id:
        self.image = resizeImage(self.image)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"
        app_label = "main"

    def __str__(self):
        return self.category_name


class Item(models.Model):
    item_name = models.CharField(max_length=200, unique=True)
    summary = models.CharField(max_length=200)
    content = models.TextField()
    date_published = models.DateTimeField(
        "date published", default=timezone.now
    )
    item_slug = models.CharField(max_length=200, unique=True)
    category_name = models.ForeignKey(
        Category,
        default=1,
        verbose_name="Category",
        on_delete=models.SET_DEFAULT,
    )

    @classmethod
    def create(cls, dictionary):
        """
        Class method to instantiate Item objects with dictionaries.
        """
        return cls(**dictionary)

    def json(self):
        """
        Returns class attributes as a dictionary.
        """
        return {
            "item_name": self.item_name,
            "summary": self.summary,
            "content": self.content,
            "date_published": self.date_published,
            "item_slug": self.item_slug,
            "category_name": self.category_name,
        }

    def save(self, *args, **kwargs):
        super(Item, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Items"
        app_label = "main"

    def __str__(self):
        return self.item_name
