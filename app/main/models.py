import logging
import sys
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils import timezone
from PIL import Image

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)

# Global variables
UPLOADS_FOLDER_PATH = "images/"
THUMBNAIL_SIZE = (500, 500)
CROP_SIZE = (300, 300)


def resizeImage(uploadedImage):
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

    def save(self, *args, **kwargs):
        if not self.id:
            try:
                self.image = resizeImage(self.image)
            except Exception as e:
                logger.warning(
                    f"Exception occured within image processing function. \
                    Error: {e}"
                )
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

    class Meta:
        verbose_name_plural = "Items"
        app_label = "main"

    def __str__(self):
        return self.item_name
