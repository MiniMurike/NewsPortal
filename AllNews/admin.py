from django.contrib import admin
from .models import Post, Author, Category, Comment, CommentReaction


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'rating', 'author')
    list_filter = ('rating', 'date', 'post_category')
    search_fields = ('title', 'author')


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(CommentReaction)
