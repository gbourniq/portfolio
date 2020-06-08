import logging
import sys
from io import BytesIO
from typing import List, Union

from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import BadHeaderError, send_mail
from django.db import models
from django.utils import timezone
from PIL import Image

from app.static_settings import EMAIL_HOST_USER

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


def get_registered_emails() -> Union[List[str], None]:
    """
    Retrives email addresses of registered users.
    """
    registered_email_addresses = [
        user.email for user in User.objects.all() if user.email
    ]
    if registered_email_addresses is not None:
        return registered_email_addresses
    return None


def send_email_notification_to_users(
    subject: str, message: str, from_email: str = EMAIL_HOST_USER
) -> None:
    """
    Send an email notification to registered users.
    """

    registered_emails = get_registered_emails()

    if not registered_emails:
        logger.warning(f"No registered emails found")
        return None

    try:
        [
            send_mail(subject, message, from_email, [to_email])
            for to_email in registered_emails
        ]
        logger.info(
            f"Email notification sent successfully to {registered_emails}"
        )
    except BadHeaderError:
        logger.warning(f"Email function {send_mail} returned BadHeaderError")


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
        send_email_notification_to_users(
            subject=f"[Tari Kitchen] New Category added!",
            message=f"A new category '{self.category_name}' has been added! Check it out here... https://www.tari.kitchen/items/{self.category_name}",
        )

    class Meta:
        verbose_name_plural = "Categories"
        app_label = "main"

    def __str__(self):
        return self.category_name


class Item(models.Model):
    item_name = models.CharField(max_length=200, unique=True)
    summary = models.CharField(max_length=200)
    image = models.ImageField(upload_to=UPLOADS_FOLDER_PATH)
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

    def save(self, *args, **kwargs):
        """
        Overrides the save method to notify all registered users
        that a new item has been added
        """
        super(Item, self).save(*args, **kwargs)
        send_email_notification_to_users(
            subject=f"[Tari Kitchen] New Item added!",
            message=f"A new item '{self.item_name}' has been added! Check it out here... https://www.tari.kitchen/items/{str(self.category_name)}/{self.item_name}",
        )

    class Meta:
        verbose_name_plural = "Items"
        app_label = "main"

    def __str__(self):
        return self.item_name
