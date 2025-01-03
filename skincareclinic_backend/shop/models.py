from django.db import models
from django.utils.text import slugify
from PIL import Image
import os
from django.conf import settings
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
    
    def __str__(self):
        return self.name
    

class Brand(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'brand'
        verbose_name_plural = 'brands'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(Brand, self).save(*args, **kwargs)
    
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/')
    thumbnail = models.ImageField(upload_to='products/', blank=True)
    available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            brand_name = slugify(self.brand.name) if self.brand else ''
            slug = f'{brand_name}-{base_slug}'
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f'{brand_name}-{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super(Product, self).save(*args, **kwargs)



        if self.image and not self.thumbnail:
            img = Image.open(self.image)
            img.thumbnail((300, 300), Image.Resampling.LANCZOS)
            thumb_io = BytesIO()
            img.save(thumb_io, img.format)
            thumb_io.seek(0)
            thumb_name = os.path.basename(self.image.name)
            mime_type = f'image/{img.format.lower()}'
            self.thumbnail = InMemoryUploadedFile(
                thumb_io,
                'ImageField',
                thumb_name,
                mime_type,
                thumb_io.tell(),
                None
            )


        super(Product, self).save(*args, **kwargs)

    def get_thumbnail(self):
        if self.thumbnail:
            return "http://127.0.0.1:8000" + self.thumbnail.url
        return 'https://placehold.co/300'
    
    def get_image(self):
        if self.image:
            return "http://127.0.0.1:8000" + self.image.url
        return 'https://placehold.co/400'

    
    
    def __str__(self):
        return self.name
