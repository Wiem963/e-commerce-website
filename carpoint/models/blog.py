from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    publish_date = models.DateField()
    image = models.ImageField(upload_to='blog/')
    excerpt = models.CharField(max_length=512, blank=True)

    def __str__(self):
        return self.title
