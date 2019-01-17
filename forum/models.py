from django.db import models

from card.models import UserProfile

class Article(models.Model):
    title = models.CharField(max_length=255)
    #topic
    content = models.TextField(default="")
    publish_date = models.DateTimeField(auto_now_add=True, null=True)
    publisher = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.DO_NOTHING,
                                related_name='article_publisher')

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField(default="")
    publish_date = models.DateTimeField(auto_now_add=True, null=True)
    article = models.ForeignKey("Article", blank=True, null=True, on_delete=models.DO_NOTHING,
                                related_name='comment_article')
    comment = models.ForeignKey("Comment", blank=True, null=True, on_delete=models.DO_NOTHING,
                                related_name='comment_comment')
    publisher = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.DO_NOTHING,
                                  related_name='comment_publisher')

    def __str__(self):
        return self.content
