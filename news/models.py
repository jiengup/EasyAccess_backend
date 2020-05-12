from django.db import models


# Create your models here.
class NewCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    thumbnail = models.URLField()
    original_url = models.URLField()
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now=True)
    total_stars = models.IntegerField()
    category = models.ForeignKey(
        "NewCategory",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    author = models.ForeignKey(
        "myauth.User",
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_time']


class Comment(models.Model):
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    total_star = models.IntegerField()
    news = models.ForeignKey(
        "News",
        on_delete=models.CASCADE,
        related_name='comments_to_news',
    )
    author = models.ForeignKey(
        'myauth.User',
        on_delete=models.CASCADE,
        related_name='author_of_comment'
    )

    def __str__(self):
        return str(self.id) + 'of' + str(self.news)

    class Meta:
        ordering = ['-pub_time']


class Banner(models.Model):
    image_url = models.URLField()
    priority = models.IntegerField(default=0)
    link_to = models.URLField()
    pub_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.link_to)

    class Meta:
        ordering = ['-priority']
