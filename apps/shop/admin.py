from django.contrib import admin

from .models import Category, Product, ProductImage, Review, ReviewImage

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("slug", "name", "parent", "image")
    list_filter = ("parent",)
    search_fields = ("slug", "name")



class ProductImageInline(admin.StackedInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    list_display = ("slug", "name", "price", "size", "color", "created")
    list_filter = ("category", "price", "size", "color")
    sortable_by = ("creted",)
    search_fields = ("slug", "name", "description")
    inlines = (ProductImageInline, )


class ReviewImageInline(admin.StackedInline):
    model = ReviewImage


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("slug", "product", "user", "stars")
    list_filter = ("stars", "product", "user")
    sortable_by = ("created", )
    search_fields = ("slug", "text")
    inlines = (ReviewImageInline, )



admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
