from django.contrib import admin
from .models import Food, Order

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available')
    list_filter = ('category', 'available')
    search_fields = ('name', 'category')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('food', 'quantity', 'total_price')
    search_fields = ('food__name',)