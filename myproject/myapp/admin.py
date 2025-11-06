from django.contrib import admin
from .models import Post, Category, ShopCategory, ShopProduct

@admin.register(Post)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'author', 'created_at')
    list_editable = ('body', 'author')
    ordering = ('-created_at',)


class ObjectInline(admin.TabularInline):
    model = Post
    fields = ('title', 'body', 'author')
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [ObjectInline]

#Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop-Shop


@admin.register(ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):
    list_display = ('name_Shop', 'price_Shop')
    list_filter = ('in_stock_Shop', 'category_Shop')
    search_fields = ('name_Shop',)

@admin.register(ShopCategory)
class ShopCategoryAdmin(admin.ModelAdmin):
    list_display = ('name_Shop',)
    search_fields = ('name_Shop',)



# music-music-music-music-music-music-music-music-music-music-music-music-music-music-music-music-music-music-music-music-music-music-music-music
from .models import MusicArtist, MusicAlbum, MusicSong, MusicGenre



@admin.register(MusicArtist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("id", "name_music")
    search_fields = ("name_music",)


@admin.register(MusicAlbum)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("id", "title_music", "artist_music")
    search_fields = ("title_music",)


@admin.register(MusicSong)
class SongAdmin(admin.ModelAdmin):
    list_display = ("id", "title_music", "artist_music", "album_music")
    search_fields = ("title_music",)

@admin.register(MusicGenre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name_music")
