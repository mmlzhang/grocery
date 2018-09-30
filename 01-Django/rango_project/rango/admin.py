from django.contrib import admin
from rango.models import Category, Page


class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'views', 'likes', 'slug')
    ordering = ('name',)
    search_fields = ('name',)  # 搜索


admin.site.register(Category, CategoryAdmin)


class PageAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'url', 'views')
    ordering = ('title',)
    search_fields = ('title',)  # 搜索


admin.site.register(Page, PageAdmin)


