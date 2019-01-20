from django.contrib import admin
from forum.models import Article, Comment

class ArticleAdmin(admin.ModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    pass



admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)