from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from managment.forms import PersonForm, CategoryForm
from managment.models import Person, Category


@login_required
def category(request):
    persons = Person.objects.filter(user=request.user)
    categories = Category.objects.filter(user=request.user)
    person_form = PersonForm()
    category_form = CategoryForm()

    if request.method == 'POST':
        if 'person_delete' in request.POST:
            person_delete(request)
        elif 'edit_person' in request.POST:
            edit_person(request)
        elif 'add_person' in request.POST:
            add_person(request)
        elif 'category_delete' in request.POST:
            category_delete(request)
        elif 'edit_category' in request.POST:
            edit_category(request)
        elif 'add_category' in request.POST:
            add_category(request)

    context = {
        'person_form': person_form,
        'category_form': category_form,
        'persons': persons,
        'categories': categories
    }
    return render(request, 'category.html', context)


def person_delete(request):
    person_id = request.POST.get('person_id')
    if person_id:
        Person.objects.filter(id=person_id).delete()
        return redirect('category')


def edit_person(request):
    person_id = request.POST.get('person_id')
    new_name = request.POST.get('person_name')
    if person_id and new_name:
        person = get_object_or_404(Person, id=person_id, user=request.user)
        person.person_name = new_name
        person.save()
        return redirect('category')


def add_person(request):
    person_form = PersonForm(request.POST)
    if person_form.is_valid():
        new_person = person_form.save(commit=False)
        new_person.user = request.user
        new_person.save()
        return redirect('category')


def category_delete(request):
    category_id = request.POST.get('category_id')
    if category_id:
        Category.objects.filter(id=category_id).delete()
        return redirect('category')


def edit_category(request):
    category_id = request.POST.get('category_id')
    new_category_name = request.POST.get('category_name')
    if category_id and new_category_name:
        category = get_object_or_404(Category, id=category_id, user=request.user)
        category.category_name = new_category_name
        category.save()
        return redirect('category')


def add_category(request):
    category_form = CategoryForm(request.POST)
    if category_form.is_valid():
        new_category = category_form.save(commit=False)
        new_category.user = request.user
        new_category.save()
        return redirect('category')
