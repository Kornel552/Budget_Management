from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .forms import PersonForm, CategoryForm, PlanForm, ElementForm
from .models import Plan, Person, Category, Element
from django.db.models import Sum
from datetime import date, datetime
import calendar


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
    if not request.user.is_authenticated:
        return render(request, 'home.html')

    plans = Plan.objects.filter(user=request.user)
    plan_form = PlanForm(request.POST)

    if request.method == 'POST':
        if 'plan_delete' in request.POST:
            plan_id = request.POST.get('plan_id')
            if plan_id:
                Plan.objects.filter(id=plan_id, user=request.user).delete()
                return redirect('/')
        elif plan_form.is_valid():
            new_plan = plan_form.save(commit=False)
            new_plan.user = request.user
            new_plan.save()
            return redirect('/')
        elif 'rename' in request.POST:
            plan_id = request.POST.get('rename_id')
            new_name = request.POST.get('rename_name')
            if plan_id and new_name:
                Plan.objects.filter(id=plan_id, user=request.user).update(plan_name=new_name)
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

    # Pobierz zakres dat z żądania GET
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Jeśli nie podano zakresu dat, ustaw na pierwszy i ostatni dzień bieżącego miesiąca
    if not start_date_str or not end_date_str:
        today = date.today()
        first_day = today.replace(day=1)
        last_day = today.replace(day=calendar.monthrange(today.year, today.month)[1])
        start_date = first_day
        end_date = last_day
    else:
        # Konwertuj stringi na obiekty date
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    # Pobierz wybrane osoby z żądania GET
    person_ids = request.GET.getlist('person')

    # Filtrowanie elementów na podstawie planu, zakresu dat i wybranych osób
    elements = Element.objects.filter(
        user=request.user,
        plan_id=charts_id,
        date_added__gte=start_date,
        date_added__lte=end_date
    )

    sum_list = []
    for i in elements:
        sum_list.append(i.cost)
    sum_list = sum(sum_list)

    if person_ids:
        elements = elements.filter(person__id__in=person_ids)
        sum_list = []
        for i in elements:
            sum_list.append(i.cost)
        sum_list = sum(sum_list)


    # Grupowanie i sumowanie kosztów według kategorii i osób
    category_person_costs = elements.values('category__category_name', 'person__person_name').annotate(total_cost=Sum('cost'))

    # Lista unikalnych kategorii i osób
    categories = list(elements.values_list('category__category_name', flat=True).distinct())
    persons = list(elements.values_list('person__person_name', flat=True).distinct())

    # Przygotowanie danych do wykresu
    data = {category: {person: 0 for person in persons} for category in categories}

    for item in category_person_costs:
        category_name = item['category__category_name']
        person_name = item['person__person_name']
        total_cost = item['total_cost']
        data[category_name][person_name] = float(total_cost)

    context = {
        'charts_id': charts_id,
        'categories': categories,
        'persons': persons,
        'data': data,
        'elements': elements,
        'sum_list': sum_list,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'all_persons': Person.objects.filter(user=request.user),
        'selected_persons': person_ids,
    }
    return render(request, 'charts.html', context)


@login_required
def elements(request):
    plans = Plan.objects.filter(user=request.user)
    plan_id = request.GET.get('plan_id')
    categories = Category.objects.filter(user=request.user)
    persons = Person.objects.filter(user=request.user)
    table_rows = []
    num_categories = 0
    should_scroll_large = False
    should_scroll_small = False

    if request.method == 'POST':
        if 'edit_element' in request.POST:
            element_id = request.POST.get('element_id')
            element_instance = get_object_or_404(Element, id=element_id, user=request.user)
            element_form = ElementForm(request.POST, instance=element_instance)
            if element_form.is_valid():
                element_form.save()
                return redirect(f'/elements/?plan_id={plan_id}')
        elif 'delete_element' in request.POST:
            id_element = request.POST.get('id_element')
            if id_element:
                Element.objects.get(id=id_element).delete()
                return redirect(f'/elements/?plan_id={plan_id}')
        elif 'add_element' in request.POST:
            add_element_form = ElementForm(request.POST)
            if add_element_form.is_valid():
                new_element = add_element_form.save(commit=False)
                new_element.user = request.user
                new_element.plan_id = plan_id
                new_element.save()
                return redirect(f'/elements/?plan_id={plan_id}')

    if plan_id:
        elements = Element.objects.filter(user=request.user, plan_id=plan_id)
        elements_by_category = {}
        for element in elements:
            category_name = element.category.category_name
            if category_name not in elements_by_category:
                elements_by_category[category_name] = []
            elements_by_category[category_name].append(element)

        category_names = list(elements_by_category.keys())
        num_categories = len(category_names)

        should_scroll_large = num_categories > 6
        should_scroll_small = num_categories > 3

        if elements_by_category:
            max_elements = max((len(elist) for elist in elements_by_category.values()), default=0)
            for i in range(max_elements):
                row = []
                for category in category_names:
                    elist = elements_by_category.get(category, [])
                    if len(elist) > i:
                        row.append(elist[i])
                    else:
                        row.append(None)
                table_rows.append(row)
        else:
            table_rows = []
    else:
        category_names = []
        table_rows = []

    return render(request, 'elements.html', {
        'plans': plans,
        'plan_id': plan_id,
        'selected_plan_id': int(plan_id) if plan_id else None,
        'categories': categories,
        'category_names': category_names,
        'table_rows': table_rows,
        'persons': persons,
        'num_categories': num_categories,
        'should_scroll_large': should_scroll_large,
        'should_scroll_small': should_scroll_small,
    })


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
                new_plan = person_form.save(commit=False)
                new_plan.user = request.user
                new_plan.save()
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
