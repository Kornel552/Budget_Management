from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .forms import PersonForm, CategoryForm, PlanForm
from .models import Plan, Person, Category, Element


def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request, "Username already taken!")
            return redirect('/register/')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password)
        user.save()
        messages.info(request, "Account created Successfully!")
        return redirect('/register/')
    return render(request, 'login/register.html')


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/login/')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/')
    return render(request, 'login/login.html')


def logout_page(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/')
    else:
        return redirect('/')


def home(request):
    plans = Plan.objects.filter(user=request.user)
    plan_form = PlanForm(request.POST)

    if request.method == 'POST':
        if 'plan_delete' in request.POST:
            plan_id = request.POST.get('plan_id')
            if plan_id:
                Plan.objects.get(id=plan_id).delete()
                return redirect('/')
        elif plan_form.is_valid():
            user = plan_form.save(commit=False)
            user.user = request.user
            user.save()
            return redirect('/')
    else:
        plan_form = PlanForm()

    context = {
        'plans': plans,
        'plan_form': plan_form
    }
    return render(request, 'home.html', context)


@login_required
def charts(request, item_id):
    charts_id = item_id

    context = {
        'charts_id': charts_id
    }
    return render(request, 'charts.html', context)


@login_required
def category(request):
    persons = Person.objects.filter(user=request.user)
    categories = Category.objects.filter(user=request.user)
    person_form = PersonForm()
    category_form = CategoryForm()

    if request.method == 'POST':
        if 'person_delete' in request.POST:
            person_id = request.POST.get('person_id')
            if person_id:
                Person.objects.get(id=person_id).delete()
                return redirect('category')

        elif 'edit_person' in request.POST:
            person_id = request.POST.get('person_id')
            new_name = request.POST.get('person_name')
            if person_id and new_name:
                person = Person.objects.get(id=person_id, user=request.user)
                person.person_name = new_name
                person.save()
                return redirect('category')

        elif 'add_person' in request.POST:
            person_form = PersonForm(request.POST)
            if person_form.is_valid():
                user = person_form.save(commit=False)
                user.user = request.user
                user.save()
                return redirect('category')

        elif 'category_delete' in request.POST:
            category_id = request.POST.get('category_id')
            if category_id:
                Category.objects.get(id=category_id).delete()
                return redirect('category')

        elif 'edit_category' in request.POST:
            category_id = request.POST.get('category_id')
            new_category = request.POST.get('category_name')
            if category_id and new_category:
                category = Category.objects.get(id=category_id, user=request.user)
                category.category_name = new_category
                category.save()
                return redirect('category')

        elif 'add_category' in request.POST:
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                user = category_form.save(commit=False)
                user.user = request.user
                user.save()
                return redirect('category')

    context = {
        'person_form': person_form,
        'category_form': category_form,
        'persons': persons,
        'categories': categories
    }
    return render(request, 'category.html', context)
