from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Brand)
admin.site.register(models.Product)
admin.site.register(models.Color)
admin.site.register(models.Categories)
admin.site.register(models.Filter_Price)
admin.site.register(models.User_Profile)
admin.site.register(models.Order_Item)
admin.site.register(models.Address)
admin.site.register(models.Payment)



@admin.register(models.Order)

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id','user','ordered','paid','ordered_date','address','payment')

