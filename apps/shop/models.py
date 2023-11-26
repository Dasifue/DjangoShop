from collections.abc import Iterable
from django.db import models
from django.db import IntegrityError

from ..account.utils import slugify


class Category(models.Model):
    slug = models.SlugField(max_length=100, null=False, unique=True)
    name = models.CharField("Category name", max_length=25)
    image = models.ImageField("Image", upload_to="category/", default="default/default-category.png")
    description = models.TextField("Description", blank=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="child_categories", verbose_name="Parent category")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    

    def save(self, *args, **kwargs) -> None:
        while True:
            self.slug = slugify(value=self.name)
            try:
                return super().save(*args, **kwargs)
            except IntegrityError:
                continue
    


class ProductSizes(models.Model):
    size = models.CharField("Size", max_length=5)
    
    class Meta:
        verbose_name = "Size"
        verbose_name_plural = "Sizes"


    def __str__(self):
        return self.size


class ProductColors(models.Model):
    color = models.CharField("Color", max_length=25)

    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colors"


    def __str__(self):
        return self.color


class Product(models.Model):
    slug = models.SlugField("Slug", max_length=100, null=False, unique=True)
    name = models.CharField("Product name", max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="products", null=True, blank=False, verbose_name="Category")
    price = models.DecimalField("Price", max_digits=7, decimal_places=2)
    discount = models.PositiveSmallIntegerField("Discount", blank=True, default=0)
    sizes = models.ManyToManyField(ProductSizes, related_name="products")
    colors = models.ManyToManyField(ProductColors, related_name="products")
    description = models.TextField("Description")
    created = models.DateTimeField("Date created", auto_now_add=True)
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name
    

    @property
    def stars(self):
        reviews = self.reviews.all()
        stars = sum((review.stars for review in reviews)) / len(reviews)
        return stars
    
    @property
    def total_price(self):
        price = float(self.price)
        return price - (price * (self.discount / 100))

    
    def save(self, *args, **kwargs) -> None:
        while True:
            self.slug = slugify(value=self.name)
            try:
                return super().save(*args, **kwargs)
            except IntegrityError:
                continue
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name="Product")
    image = models.ImageField("Image", upload_to="products/", default="default/default-product.jpg")

    class Meta:
        verbose_name = "Product image"
        verbose_name_plural = "Product images"

    def __str__(self):
        return self.product.name
    

class Review(models.Model):
    STARS = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    slug = models.SlugField("Slug", max_length=100, null=False, unique=True)
    user = models.ForeignKey("account.User", on_delete=models.SET_NULL, related_name="reviews", null=True, verbose_name="Owner")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews", verbose_name="Product")
    text = models.TextField("Text")
    stars = models.PositiveSmallIntegerField("Stars", choices=STARS, null=True, blank=True)
    created = models.DateTimeField("Created at", auto_now_add=True)
    updated = models.DateTimeField("Updated at", auto_now=True)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    
    def save(self, *args, **kwargs) -> None:
        while True:
            self.slug = slugify(value=f"{self.user.username}{self.product.name}")
            try:
                return super().save(*args, **kwargs)
            except IntegrityError:
                continue


class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="images", verbose_name="Review")
    image = models.ImageField("Image", upload_to=f"reviews/", null=False, blank=True)

    class Meta:
        verbose_name = "Review image"
        verbose_name_plural = "Review images"


class PromoCode(models.Model):
    name = models.CharField("Name", max_length=20)
    discount = models.PositiveSmallIntegerField("Discount")
    created = models.DateField("Created at", auto_now_add=True)
    expired = models.DateField("Expired at")

    class Meta:
        verbose_name = "Promo code"
        verbose_name_plural = "Promo codes"
    
    def __str__(self):
        return self.name


class Cart(models.Model):
    ACTIVE = "active"
    FINISHED = "finished"
    WAITING = "waiting"
    CHOISES = (
        (ACTIVE, "Active"),
        (FINISHED, "Finished"),
        (WAITING, "Waiting"),
    )

    user = models.ForeignKey("account.User", on_delete=models.CASCADE, related_name="carts", verbose_name="User")
    status = models.CharField("Status", max_length=10, choices=CHOISES, default=ACTIVE)
    promo = models.ForeignKey(PromoCode, null=True, on_delete=models.SET_NULL, related_name="carts", verbose_name="Promo code")
    created = models.DateTimeField("Created at", auto_now_add=True)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    @property
    def subtotal(self):
        subtotal = sum(product.total_price for product in self.cart_products.all())
        return subtotal
    
    @property
    def discount(self):
        if self.promo is not None:
            discount = self.subtotal * self.promo.discount / 100
        else:
            discount = 0
        return discount
    
    @property
    def total(self):
        total = self.subtotal - self.discount + 10
        return total



class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_products", verbose_name="Cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_products", verbose_name="Product")
    quantity = models.PositiveSmallIntegerField("Quantiy")
    color = models.CharField("Color", max_length=50)
    size = models.CharField("Size", max_length=20)

    class Meta:
        verbose_name = "Cart Product"
        verbose_name_plural = "Cart Products"


    @property
    def total_price(self):
        price = self.product.total_price
        total_price = self.quantity * price

        return total_price