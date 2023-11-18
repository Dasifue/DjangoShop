from django.contrib import admin

from .models import Category, Product, ProductImage, Review, ReviewImage, ProductColors, ProductSizes, Cart, CartProduct, PromoCode

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("slug", "name", "parent", "image")
    list_filter = ("parent",)
    search_fields = ("slug", "name")
    exclude = ("slug", )
    list_display_links = ("name",)




class ProductImageInline(admin.StackedInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    list_display = ("slug", "name", "price", "created")
    list_display_links = ("name",)
    list_filter = ("category", "price", "sizes", "colors")
    sortable_by = ("creted",)
    search_fields = ("slug", "name", "description")
    inlines = (ProductImageInline, )
    exclude = ("slug", )


class ReviewImageInline(admin.StackedInline):
    model = ReviewImage


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("slug", "product", "user", "stars")
    list_filter = ("stars", "product", "user")
    sortable_by = ("created", )
    search_fields = ("slug", "text")
    inlines = (ReviewImageInline, )
    exclude = ("slug", )


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ("name", "discount", "created", "expired")
    list_filter = ("discount", "created", "expired")
    search_fields = ("name", )


class CartProductInline(admin.StackedInline):
    model = CartProduct


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "promo", "created")
    list_filter = ("status", "promo")
    search_fields = ("user", "created")
    inlines = (CartProductInline,)
    


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ProductColors)
admin.site.register(ProductSizes)