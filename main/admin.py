from django.contrib import admin

from .models import (
    Province,
    District,
    Commune,
    User,
    Product,
    Order,
    OrderProduct,
    Category,
    ProductImage,
    CartProduct,
)

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(CartProduct)
