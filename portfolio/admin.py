from django.contrib import admin
from .models import Category, Photos

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Photos)
class PhotosAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'criado_em', 'author', 'preco', 'esta_publicado']
    list_display_links = ['titulo', 'criado_em']
    search_fields = ['id', 'titulo', 'criado_em', 'descricao', 'slug', 'historia']
    list_filter = ['category', 'author', 'esta_publicado']
    list_per_page = 15
    list_editable = ['esta_publicado']
    ordering = ['criado_em', 'author']
    prepopulated_fields = {
        "slug":('titulo',)
    }
