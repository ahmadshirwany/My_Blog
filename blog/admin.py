from django.contrib import admin
from .models import Post, Author, Tag, comments


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('title', 'author', 'Date', 'tag')
    list_display = ("id", "title", "author", "Date")


class commentsadmin(admin.ModelAdmin):
    list_display = ("username", "post", "published_at")


admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(comments, commentsadmin)
