from django.db import models
from django.utils.text import slugify


# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name + "(" + self.email + ")"


class Tag(models.Model):
    caption = models.CharField(max_length=50)

    def __str__(self):
        return self.caption


class Post(models.Model):
    post_id = models.IntegerField(auto_created=True, editable=True, null=True)
    title = models.CharField(max_length=50)
    excerpt = models.CharField(max_length=500)
    link = models.URLField(blank=True)
    image_name = models.ImageField(upload_to="posts", null=True)
    Date = models.DateTimeField(auto_now_add=False)
    slug = models.SlugField(default="", blank=True, null=False, db_index=True)
    content = models.TextField(blank=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, )
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, *kwargs)


class comments(models.Model):
    username = models.CharField(max_length=50)
    user_email = models.EmailField()
    comment_text = models.TextField(max_length=10000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    published_at = models.DateTimeField(auto_now=True)
