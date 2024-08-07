from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(verbose_name="name", max_length=50)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    @property
    def get_first_six_clothes(self):
        clothes = self.clothes.all()[:6]
        return clothes

class Clothes(models.Model):
    image = models.ImageField(verbose_name="image", upload_to="clothes")
    name = models.CharField(verbose_name="name", max_length=100)
    description = models.TextField(verbose_name="description")
    price = models.DecimalField(verbose_name="price", max_digits=7, decimal_places=2, default=1, blank=True)
    discount = models.SmallIntegerField(verbose_name="discount", default=0, blank=True)
    uploaded = models.DateTimeField(verbose_name="uploaded date", auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="clothes")

    class Meta:
        verbose_name_plural = "Clothes"

    def __str__(self):
        return self.name
    
    @property
    def price_with_discount(self):
        return self.price - (self.price * self.discount / 100)
