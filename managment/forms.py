from django import forms
from . import models


class PlanForm(forms.ModelForm):
    class Meta:
        model = models.Plan
        fields = ['plan_name']
        widgets = {
            'plan_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PersonForm(forms.ModelForm):
    class Meta:
        model = models.Person
        fields = ['person_name']
        widgets = {
            'person_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ['category_name', ]
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ElementForm(forms.ModelForm):
    class Meta:
        model = models.Element
        fields = ['person', 'category', 'element_name', 'cost', 'date_added']
        widgets = {
            'element_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_added': forms.DateInput(attrs={'type': 'date'})
        }
