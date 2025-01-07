from django.db import models
from django.utils.text import slugify

# Create your models here.
class DeliveryCategory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'delivery category'
        verbose_name_plural = 'delivery categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(DeliveryCategory, self).save(*args, **kwargs)
    
    
    def __str__(self):
        return self.name
    

class Delivery(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    category = models.ForeignKey(DeliveryCategory, on_delete=models.CASCADE, related_name='deliveries', blank=True, null=True)
    weight_from = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    weight_to = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price = models.PositiveIntegerField()

    class Meta:
        ordering = ('name',)
        verbose_name = 'delivery'
        verbose_name_plural = 'deliveries'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Delivery, self).save(*args, **kwargs)

    def __str__(self):
        weight_range = ""
        if self.weight_from is not None and self.weight_to is not None:
            weight_range = f" ({self.weight_from} - {self.weight_to}kg)"
        elif self.weight_from is not None:
            weight_range = f" ({self.weight_from}+)"
        return f"{self.name}-{self.category.name} {weight_range}"
