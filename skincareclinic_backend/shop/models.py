from django.db import models
from django.utils.text import slugify
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill



# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True,editable=False)
    image = models.ImageField(upload_to='categories/',blank=True, null=True)
    thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(300, 300)], format='WEBP', options={'quality': 85})
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def get_thumbnail(self):
        try:
            return settings.SITE_URL + self.thumbnail.url
        except ValueError:
            return 'https://placehold.co/300'
        
   
    def get_image(self):
        try:
            return settings.SITE_URL + self.image.url
        except ValueError:
            return 'https://placehold.co/400'
        
    

    
    
    def __str__(self):
        return self.name
    

class Collections(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True,editable=False)
    image = models.ImageField(upload_to='collections/',blank=True, null=True)
    thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(300, 300)], format='WEBP', options={'quality': 85})
    class Meta:
        ordering = ('name',)
        verbose_name = 'collection'
        verbose_name_plural = 'collections'

    def save(self, *args, **kwargs):
        if not self.pk or Collections.objects.get(pk=self.pk).name != self.name:
           self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def get_thumbnail(self):
        try:
            return settings.SITE_URL + self.thumbnail.url
        except ValueError:
            return 'https://placehold.co/300'
        
   
    def get_image(self):
        try:
            return settings.SITE_URL + self.image.url
        except ValueError:
            return 'https://placehold.co/400'
        
    

    
    
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
        if not self.pk or Brand.objects.get(pk=self.pk).name != self.name:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)
    
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    collection = models.ManyToManyField(Collections,related_name='products', blank=True)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/',blank=True, null=True)
    thumbnail = ImageSpecField(source='image', processors = [ResizeToFill(300, 300)],format='WEBP',options={'quality': 85})                               
    available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('-created',)


    def generate_slug(self):
        base_slug = slugify(self.name)
        brand_name = slugify(self.brand.name) if self.brand else ''
        slug = f'{brand_name}-{base_slug}'
        counter = 1
        temp_slug = slug
        while Product.objects.filter(slug=temp_slug).exists():
            temp_slug = f'{slug}-{counter}'
            counter += 1

        return temp_slug

    def save(self, *args, **kwargs):
        if not self.pk or Product.objects.get(pk=self.pk).name != self.name:
            self.slug = self.generate_slug()
        super().save(*args, **kwargs)




    def get_thumbnail(self):
        try:
            return settings.SITE_URL + self.thumbnail.url
        except ValueError:
            return 'https://placehold.co/300'
        
   
    def get_image(self):
        try:
            return settings.SITE_URL + self.image.url
        except ValueError:
            return 'https://placehold.co/400'
        
    
    
    def __str__(self):
        brand_name = self.brand.name if self.brand else ''
        return f'{brand_name} - {self.name}' if brand_name else self.name
