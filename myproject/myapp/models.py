
from django.db import models
from django.conf import settings



from datetime import datetime
# Получаем текущую дату и время
now = datetime.now()
# Форматируем дату и время в нужный вид
formatted_date_time = now.strftime("%d.%m.%y %H:%M")
print(formatted_date_time)



# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100, blank=False)
    body = models.TextField(blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)


class Category(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name





#Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop

class ShopProduct(models.Model):
    name_Shop = models.CharField(max_length=100)
    description_Shop = models.TextField(blank=True)
    price_Shop = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock_Shop = models.BooleanField(default=True)
    category_Shop = models.ForeignKey('ShopCategory', on_delete=models.SET_NULL, null=True, blank=True)

    image_Shop = models.ImageField(upload_to='product_images/', blank=True, null=True)

#     def __str__(self):
#         return self.name_Shop
#
#
# class ShopImage(models.Model):
#     image_Shop = models.ImageField(upload_to='product_images/')
#
#     def __str__(self):
#         return f'{self.image.url}'


class ShopCategory(models.Model):
    name_Shop = models.CharField(max_length=100)

    def __str__(self):
        return self.name_Shop



#music-music-music-music-music-music-music-music-music-music-music-music-music-music-music-music-music-music-music-music-music-music-music-music

class MusicGenre(models.Model):
    name_music = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name_music


class MusicArtist(models.Model):
    name_music = models.CharField(max_length=200)
    image_music = models.ImageField(upload_to='artists/', blank=True, null=True)
    date_music = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name_music

class MusicAlbum(models.Model):
    title_music = models.CharField(max_length=200)
    artist_music = models.ForeignKey(MusicArtist, on_delete=models.CASCADE, related_name='albums')
    cover_music = models.ImageField(upload_to='albums/', blank=True, null=True)
    release_year_music = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.title_music} — {self.artist_music.name_music}"


class MusicSong(models.Model):
    title_music = models.CharField(max_length=200)
    artist_music = models.ForeignKey(MusicArtist, on_delete=models.CASCADE, related_name='songs')
    album_music = models.ForeignKey(MusicAlbum, on_delete=models.SET_NULL, blank=True, null=True, related_name='songs')
    genre_music = models.ForeignKey(MusicGenre, on_delete=models.SET_NULL, blank=True, null=True)
    audio_file_music = models.FileField(upload_to='songs/', blank=True, null=True)

    def __str__(self):
        return f"{self.title_music} — {self.artist_music.name_music}"
