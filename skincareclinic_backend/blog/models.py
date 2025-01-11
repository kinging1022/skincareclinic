from django.db import models
from django.utils.text import slugify



# Create your models here.
class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'blog_categories'


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(BlogCategory, self).save(*args, **kwargs)


    def __str__(self):
        return self.name



class BlogPost(models.Model):
    Category = models.ForeignKey(BlogCategory, related_name='blog', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/',blank=True, null=True)
    read_time = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-created_at',)
        

    def __str__(self):
        return self.title
    
    def get_image(self):
        if self.image:
            return "http://127.0.0.1:8000" + self.image.url
        return 'https://placehold.co/400'