from django.contrib import admin
from rango.models import Category, Page, PageAdmin, CategoryAdmin

# Register your models here.

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)


