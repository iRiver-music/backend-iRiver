from django.db import models

from Music.models import Artist, Song

# 每天訪問量


class DailyViews(models.Model):
    views_count = models.PositiveIntegerField(default=0)
    date = models.DateField(unique=True)

    def __str__(self):
        return f'Daily Views for {self.date}'

# search 次數


class SearchViews(models.Model):
    views_count = models.PositiveIntegerField(default=0)
    date = models.DateField(unique=True)

    def __str__(self):
        return f'SearchViews Views for {self.date}'

# music  =================================================================
# 每天總聽歌次數


class MusicViews(models.Model):
    views_count = models.PositiveIntegerField(default=0)
    date = models.DateField(unique=True)

    def __str__(self):
        return f'Daily Views for {self.date}'


class SongViewsCount(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Views for artists on {self.views_count}'


class ArtistViewsCount(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Views count for {self.artist} on {self.date}'


class FavSongViewsCount(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Views for artists on {self.views_count}'


# 對各種 操作的點擊次數  =================================================================


class Tab(models.Model):
    tab = models.CharField(max_length=255)

    def __str__(self):
        return self.tab


class TabViews(models.Model):
    tab = models.ForeignKey(Tab, on_delete=models.CASCADE)
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Views for tabs on {self.date}'

# 使用者裝置


class UserDevice(models.Model):
    device = models.CharField(max_length=255)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"User Device for {self.delete} count  {self.count}"


# 每天註冊量

class RegisterViews(models.Model):
    views_count = models.PositiveIntegerField(default=0)
    date = models.DateField(unique=True)

    def __str__(self):
        return f"User Device for {self.delete} count  {self.count}"
