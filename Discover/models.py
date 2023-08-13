from django.db import models

from Music.models import Style


class DiscoverTitle(models.Model):
    show_title = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'discoverTitle'

    def __str__(self):
        return self.show_title
