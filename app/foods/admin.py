# -*- coding: utf-8 -*- 
from django.contrib import admin
from models import *

### Company 
class CompanyAdmin(admin.ModelAdmin):
    pass
admin.site.register(Company,CompanyAdmin)
### Shop 
class ShopAdmin(admin.ModelAdmin):
    pass
admin.site.register(Shop,ShopAdmin)
### Customer 
class CustomerAdmin(admin.ModelAdmin):
    list_display=('user','gender',)
admin.site.register(Customer,CustomerAdmin)

### Product 
class ProductAdmin(admin.ModelAdmin):
    list_display=('company','name',)
admin.site.register(Product,ProductAdmin)

### Price
class PriceAdmin(admin.ModelAdmin):
    list_display=('shop','product','price',)
admin.site.register(Price,PriceAdmin)

### Promotion 
class PromotionAdmin(admin.ModelAdmin):
    list_display=('schedule','product','name',)
admin.site.register(Promotion,PromotionAdmin)

