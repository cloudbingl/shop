from django.contrib import admin

from df_user import models
# Register your models here.

admin.site.register(models.UserInfo)
admin.site.register(models.AddressInfo)