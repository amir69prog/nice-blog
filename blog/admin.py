from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'reading_time', 'date_created', 'date_updated')


admin.site.register(Post, PostAdmin)