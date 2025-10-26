from django.contrib import admin
# from myproject.myapp.models import Product
from .models import Post, Category


@admin.register(Post)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'author')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)