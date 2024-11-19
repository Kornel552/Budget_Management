from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from managment.forms import ElementForm
from managment.models import Plan, Person, Category, Element
from django.db.models import Q


@login_required
def elements(request):
    plans = Plan.objects.filter(user=request.user)
    plan_id = request.GET.get('plan_id')
    categories = []
    persons = []
    category_names = []
    table_rows = []
    search_query = request.GET.get('search', '').strip()

    if request.method == 'POST':
        if 'edit_element' in request.POST:
            edit_element(request.POST.get('element_id'), request.POST, request.user)
        elif 'delete_element' in request.POST:
            delete_element(request.POST.get('id_element'))
        elif 'add_element' in request.POST:
            add_element(request.POST, plan_id, request.user)

    if plan_id:
        categories = Category.objects.filter(user=request.user)
        persons = Person.objects.filter(user=request.user)
        filter_criteria = Q(user=request.user, plan_id=plan_id)

        if search_query:
            filter_criteria &= (
                Q(element_name__icontains=search_query) |
                Q(person__person_name__icontains=search_query) |
                Q(cost__icontains=search_query) |
                Q(date_added__icontains=search_query)
            )

        elements = Element.objects.filter(filter_criteria).select_related('person', 'category').order_by('-date_added')
        elements_by_category = group_elements_by_category(elements)
        category_names = list(elements_by_category.keys())
        table_rows = build_table_rows(elements_by_category, category_names)

    return render(request, 'elements.html', {
        'plans': plans,
        'plan_id': plan_id,
        'selected_plan_id': int(plan_id) if plan_id else None,
        'categories': categories,
        'category_names': category_names,
        'table_rows': table_rows,
        'persons': persons,
        'search_query': search_query,
    })


def build_filter_criteria(user, plan_id=None, search_query=None):
    criteria = Q(user=user)
    if plan_id:
        criteria &= Q(plan_id=plan_id)
    if search_query:
        criteria &= (
            Q(element_name__icontains=search_query) |
            Q(person__person_name__icontains=search_query) |
            Q(cost__icontains=search_query) |
            Q(date_added__icontains=search_query)
        )
    return criteria


def group_elements_by_category(elements):
    elements_by_category = {}
    for element in elements:
        category_name = element.category.category_name
        if category_name not in elements_by_category:
            elements_by_category[category_name] = []
        elements_by_category[category_name].append(element)
    return elements_by_category


def build_table_rows(elements_by_category, category_names):
    table_rows = []
    max_elements = max((len(elist) for elist in elements_by_category.values()), default=0)
    for i in range(max_elements):
        row = []
        for category in category_names:
            elist = elements_by_category.get(category, [])
            row.append(elist[i] if len(elist) > i else None)
        table_rows.append(row)
    return table_rows


def edit_element(element_id, data, user):
    element_instance = get_object_or_404(Element, id=element_id, user=user)
    form = ElementForm(data, instance=element_instance)
    if form.is_valid():
        form.save()


def delete_element(id_element):
    if id_element:
        Element.objects.get(id=id_element).delete()


def add_element(data, plan_id, user):
    form = ElementForm(data)
    if form.is_valid():
        new_element = form.save(commit=False)
        new_element.user = user
        new_element.plan_id = plan_id
        new_element.save()
