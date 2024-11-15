from django.contrib import admin
from . import models


class PlanAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan_name', 'created_date']


admin.site.register(models.Plan, PlanAdmin)


class PersonAdmin(admin.ModelAdmin):
    list_display = ['user', 'person_name']


admin.site.register(models.Person, PersonAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'category_name']


admin.site.register(models.Category, CategoryAdmin)


class ElementAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'person', 'category', 'element_name', 'cost', 'date_added']


admin.site.register(models.Element, ElementAdmin)
