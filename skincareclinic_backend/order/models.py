from django.db import models
from shop.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import os
from io import BytesIO
from xhtml2pdf import pisa

# Create your models here.
class Order(models.Model):
   ORDERED =  3
   RECIEVED = 0
   PROCESSED = 1
   SENT = 2

   STATUS_CHOICES = (
      (ORDERED,'Ordered'),
      (RECIEVED,'Recieved'),
      (PROCESSED,'Processed'),
      (SENT,'Sent'),
   )

   PICK_UP = 'pickup'
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
   weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
   order_amount = models.CharField(max_length=225,blank=True, null=True)
   shipping_fee = models.CharField(max_length=225, blank=True,null=True)
   order_amount_with_shipping = models.CharField(max_length=225, blank=True, null=True)
   delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default=PICK_UP)
   delivery_area = models.CharField(max_length=100, blank=True, null=True)
   paid = models.BooleanField(default=False)
   transaction_ref = models.CharField(max_length=225,null=True,blank=True,editable=False)
   shipped_date = models.DateField(blank=True, null=True)
   status = models.IntegerField( choices=STATUS_CHOICES, default=ORDERED)


   def __str__(self):
        return f"{self.full_name} - ${self.order_amount_with_shipping}"


   def send_order_created(self):
       subject = f'Order Created - Order number #{self.id}'
       message = render_to_string('emails/order_created.html', {'order':self})
       from_email = settings.DEFAULT_FROM_EMAIL
       recipient_list = [settings.BRAND_EMAIL]

       pdf = self.generate_pdf()

       email = EmailMessage(subject, message, from_email, recipient_list)
       email.content_subtype = 'html'
       email.attach(f'order_{self.id}.pdf', pdf,  'application/pdf')
       email.send()


   def send_order_sent(self):
       subject = f'Order Sent - Order number #{self.id}'
       message = render_to_string('emails/order_sent.html', {'order':self})
       from_email = settings.DEFAULT_FROM_EMAIL
       recipient_list = [self.email]

       email = EmailMessage(subject, message, from_email, recipient_list)
       email.content_subtype = 'html'
       email.send()


   def send_confirmation_email(self):
       subject = f'Order Confirmation - Order #{self.id}'
       message = render_to_string('emails/order_confirmation.html',{'order':self})
       from_email = settings.DEFAULT_FROM_EMAIL
       recipient_list = [self.email]

       #generate pdf

       pdf = self.generate_pdf()

       email = EmailMessage(subject, message, from_email, recipient_list)
       email.content_subtype = 'html'
       email.attach(f'order_{self.id}.pdf', pdf,  'application/pdf')
       email.send()

   def generate_pdf(self):
       template = render_to_string ('pdfs/order_detail.html', {'order': self})
       result = BytesIO()
       pdf = pisa.pisaDocument(BytesIO(template.encode("UTF-8")), result)
       if not pdf.err:
            return result.getvalue()
       return None

       


   

   


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.DO_NOTHING)
    price = models.CharField(max_length=225, blank=True, null=True)
    quantity = models.IntegerField(default=1)


    def __str__(self) -> str:
        date = self.order.created_at.strftime('%Y-%m-%d')
        brand_name = self.product.brand.name if self.product.brand else ''
        return f'{date} -- {brand_name} - {self.product.name} - {self.quantity} pcs'