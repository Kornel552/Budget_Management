from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from managment.models import Plan, Person, Element
from django.db.models import Sum
from datetime import date, datetime
import calendar


@login_required
def charts_choice(request):
    posts = Plan.objects.filter(user=request.user)
    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')
        if plan_id:
            return redirect('charts', item_id=plan_id)

    context = {
        'posts': posts,
    }
    return render(request, 'charts_choice.html', context)


@login_required
def charts(request, item_id):
    charts_id = item_id

    start_date, end_date = get_date_range(request)
    person_ids = request.GET.getlist('person')
    elements = filter_elements(request.user, charts_id, start_date, end_date, person_ids)
    total_cost = calculate_total_cost(elements)
    data, categories, persons = prepare_chart_data(elements)

    context = {
        'charts_id': charts_id,
        'categories': categories,
        'persons': persons,
        'data': data,
        'elements': elements,
        'sum_list': total_cost,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'all_persons': Person.objects.filter(user=request.user),
        'selected_persons': person_ids,
    }
    return render(request, 'charts.html', context)


def get_date_range(request):
    """Pobierz zakres dat z żądania GET lub ustaw domyślny zakres (bieżący miesiąc)."""
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if not start_date_str or not end_date_str:
        today = date.today()
        first_day = today.replace(day=1)
        last_day = today.replace(day=calendar.monthrange(today.year, today.month)[1])
        return first_day, last_day

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    return start_date, end_date


def filter_elements(user, plan_id, start_date, end_date, person_ids):
    """Filtruj elementy na podstawie użytkownika, planu, dat i wybranych osób."""
    elements = Element.objects.filter(
        user=user,
        plan_id=plan_id,
        date_added__gte=start_date,
        date_added__lte=end_date
    )

    if person_ids:
        elements = elements.filter(person__id__in=person_ids)

    return elements


def calculate_total_cost(elements):
    """Oblicz całkowity koszt dla danego zestawu elementów."""
    return sum(elements.values_list('cost', flat=True))


def prepare_chart_data(elements):
    """Grupuj elementy i przygotuj dane do wykresów."""
    category_person_costs = elements.values('category__category_name', 'person__person_name').annotate(total_cost=Sum('cost'))

    categories = list(elements.values_list('category__category_name', flat=True).distinct())
    persons = list(elements.values_list('person__person_name', flat=True).distinct())

    data = {category: {person: 0 for person in persons} for category in categories}

    for item in category_person_costs:
        category_name = item['category__category_name']
        person_name = item['person__person_name']
        total_cost = item['total_cost']
        data[category_name][person_name] = float(total_cost)

    return data, categories, persons
