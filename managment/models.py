from django.db import models


class Plan(models.Model):
    plan_name = models.CharField(max_length=150)

    def __str__(self):
        return self.plan_name


class Person(models.Model):
    person_name = models.CharField(max_length=50)

    def __str__(self):
        return self.person_name


class Category(models.Model):
    category_name = models.CharField(max_length=150)

    def __str__(self):
        return self.category_name


class Element(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    element_name = models.CharField(max_length=150)
    cost = models.FloatField(validators=(0, 0)) # przetestować

    def __str__(self):
        return self.element_name
