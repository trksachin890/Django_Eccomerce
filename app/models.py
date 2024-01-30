from django.db import models
from django.contrib.auth.models import AbstractUser

class Customer(AbstractUser):
    address = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=15)

    def __str__(self):
        return self.username  # Display the username in the admin site

class Product(models.Model):
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=255)
    product_price = models.FloatField(default=0)
    product_image = models.ImageField(upload_to="images")

    def __str__(self):
        return self.product_name



class Cart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.user.username}'s Cart - {self.product_id.product_name}"

class Order(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Assuming Product is your product model
    # Other fields in your Order model

   
    def total_price(self):
        return self.cart.quantity * self.product.product_price if self.cart else 0

    def __str__(self):
        return f"{self.user.username}'s Order for {self.product.product_name}"
