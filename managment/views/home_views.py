from django.shortcuts import render, redirect
from managment.forms import PlanForm
from managment.models import Plan


def home(request):
    if request.user.is_authenticated:
        plans = Plan.objects.filter(user=request.user)
        if request.method == 'POST':
            if 'plan_delete' in request.POST:
                delete_plan(request)
            elif 'rename' in request.POST:
                rename_plan(request)
            else:
                add_plan(request)
            return redirect('/')
        else:
            plan_form = PlanForm()
        context = {
            'plans': plans,
            'plan_form': plan_form
        }
        return render(request, 'home.html', context)
    return render(request, 'home.html')


def delete_plan(request):
    plan_id = request.POST.get('plan_id')
    Plan.objects.filter(id=plan_id, user=request.user).delete()


def rename_plan(request):
    plan_id = request.POST.get('rename_id')
    new_name = request.POST.get('rename_name')
    Plan.objects.filter(id=plan_id, user=request.user).update(plan_name=new_name)


def add_plan(request):
    plan_form = PlanForm(request.POST)
    if plan_form.is_valid():
        new_plan = plan_form.save(commit=False)
        new_plan.user = request.user
        new_plan.save()
