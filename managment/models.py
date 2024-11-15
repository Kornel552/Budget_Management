from django.db import models
from django.contrib.auth.models import User


class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=150)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.plan_name


class Person(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    person_name = models.CharField(max_length=50)

    def __str__(self):
        return self.person_name


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=150)

    def __str__(self):
        return self.category_name


class Element(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    element_name = models.CharField(max_length=150)
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    date_added = models.DateField()

    def __str__(self):
        return self.element_name
