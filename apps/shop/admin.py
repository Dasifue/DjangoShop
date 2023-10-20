from django.contrib import admin

from .models import Category, Product, ProductImage, Review, ReviewImage, ProductColors, ProductSizes

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



admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ProductColors)
admin.site.register(ProductSizes)