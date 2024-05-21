from django.contrib import admin
from django.utils.safestring import mark_safe
from requests import ReadTimeout
from .models import ArticleModel, Category, Comments

# Register your models here.
@admin.register(ArticleModel)
class ArticleAdmin(admin.ModelAdmin):
    fields = [
        'name', 'description', 'content', 'is_published', 'photo', 'post_photo', 'cat',
    ]
    
    readonly_fields = ['post_photo']
    # prepopulated_fields = {'slug':('name',)}
    # filter_horizontal
    list_display = ('name', 'post_photo','is_published', 'time_created', 'time_updated', 'cat' )
    ordering = [
        '-time_created', 'name'
    ]
    list_editable = ['is_published']
    list_per_page = 10
    save_on_top = True
    list_filter = [
        'cat__name', 'is_published',
    ]
    
    @admin.display(description='Изображение', ordering='content')
    def post_photo(self, article):
        if article.photo:
            return mark_safe(f"<img src='{article.photo.url}' width=50")
        return 'Без фото'
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    
    fields = ['name']
    list_display = ['name']
    ordering = ['name']
    save_on_top = True


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['article', 'text', 'author', 'created_at']
    list_filter = ['article', 'author']
    
    def post_link(self, obj: Comments):
        return mark_safe(
            f"<a href='{obj.article.get_absolute_url()}>{obj.article.name}</a>'"
        )
    post_link.allow_tags = True