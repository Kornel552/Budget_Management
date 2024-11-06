from django.contrib import admin
from . import models


class PlanAdmin(admin.ModelAdmin):
    list_display = ['plan_name']


admin.site.register(models.Plan, PlanAdmin)


class PersonAdmin(admin.ModelAdmin):
    list_display = ['person_name']


admin.site.register(models.Person, PersonAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name']


admin.site.register(models.Category, CategoryAdmin)


class ElementAdmin(admin.ModelAdmin):
    list_display = ['plan', 'person', 'category', 'element_name', 'cost']


admin.site.register(models.Element, ElementAdmin)
