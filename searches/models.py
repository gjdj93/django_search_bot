from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Search(models.Model):
    """
    A model to store the product info a user wants to search for.
    """

    name = models.CharField(max_length=255, help_text="The product name")
    url = models.CharField(max_length=1024, help_text="The url to the product")
    phrase = models.CharField(
        max_length=255,
        help_text="This phrase will be searched on the website - if the phrase is not there then the item should be in stock",
    )
    date_added = models.DateTimeField(default=timezone.now, blank=True)
    found = models.BooleanField(default=False)
    date_found = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        app_label = "searches"
        verbose_name_plural = "searches"

    def __str__(self):
        return self.name
