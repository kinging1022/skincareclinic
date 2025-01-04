from django.db import models
from shop.models import Product

# Create your models here.
class Order(models.Model):
   ORDERED = 'ordered'
   RECIEVED = 'recieved' 
   PROCESSED = 'processed'
   SENT = 'sent'

   STATUS_CHOICES = (
      (ORDERED,'Ordered'),
      (RECIEVED,'Recieved'),
      (PROCESSED,'Processed'),
      (SENT,'Sent'),
   )

   PICK_UP = 'pick_up'
   DELIVERY = 'delivery'

   DELIVERY_CHOICES = (
       (PICK_UP,'Pick Up'),
       (DELIVERY,'Delivery')
   )
   
   full_name = models.CharField(max_length=100)
   email = models.CharField(max_length=100)
   address = models.CharField(max_length=100)
   phone = models.CharField(max_length=225,blank=True, null=True)
   created_at = models.DateTimeField(auto_now_add=True)
   
   paid = models.BooleanField(default=False)
   paid_amount = models.FloatField(blank=True, null=True)
   delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default=PICK_UP)
   shipping_fee = models.FloatField(blank=True,null=True)
   transaction_ref = models.CharField(max_length=225,null=True,blank=True,editable=False)
   shipped_date = models.DateTimeField(blank=True, null=True)
   status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ORDERED)


   def __str__(self):
        return f"{self.full_name} - {self.paid_amount}"
   

   


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.DO_NOTHING)
    price = models.FloatField()
    quantity = models.IntegerField(default=1)


    def __str__(self) -> str:
        return self.id