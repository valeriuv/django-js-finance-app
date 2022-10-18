from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from . models import Income, Source
from userpreferences.models import UserPreference
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from django.http import JsonResponse


def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = Income.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Income.objects.filter(
            date__istartswith=search_str, owner=request.user) | Income.objects.filter(
            description__icontains=search_str, owner=request.user) | Income.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = income.values()    # returns a list from QuerySet
        return JsonResponse(list(data), safe=False)

@login_required(login_url='/authentication/login')
def index(request):
    income = Income.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    currency_iso = currency.split()[0]

    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency,
        'currency_iso': currency_iso,
    }
    return render(request, 'income/index.html', context)

@login_required(login_url='/authentication/login')
def income_add(request):
    sources = Source.objects.all()

    context = {
        'sources': sources
    }

    if request.method == 'GET':
        return render(request, 'income/income-add.html', context)

    elif request.method == 'POST':

        income_amount = request.POST['income-amount'] # should map to the name of the input
        income_description = request.POST['income-description'] # should map to the name of the input
        income_source = request.POST['income-source'] # should map to the name of the input
        income_date = request.POST['income-date']
        
        context = {
            'sources': sources,
            'amount': income_amount,
            'description': income_description,
            'source': income_source,
            'date': income_date
        }

        if not income_amount:
            messages.error(request, 'Income amount is required.')
            return render(request, 'income/income-add.html', context)

        if not income_description:
            messages.error(request, 'Income description is required.')
            return render(request, 'income/income-add.html', context)

        if not income_date:
            messages.error(request, 'Date of income is required.')
            return render(request, 'income/income-add.html', context)

        Income.objects.create(
            owner=request.user,
            amount=income_amount, 
            description=income_description, 
            source=income_source, 
            date=income_date)

        messages.success(request, 'Income saved successfully.')

        return redirect('income')

@login_required(login_url='/authentication/login')
def income_edit(request, pk):
    income = Income.objects.get(id=pk)
    sources = Source.objects.exclude(name=income.source)

    context = {
        'amount': income.amount,
        'description': income.description,
        'source': income.source,
        'date': str(income.date),
        'sources': sources,
        'income_id': income.id
    }

    if request.method == 'POST':

        income_amount = request.POST['income-amount'] # should map to the name of the input
        income_description = request.POST['income-description'] # should map to the name of the input
        income_source = request.POST['income-source'] # should map to the name of the input
        income_date = request.POST['income-date']
        
        context = {
            'sources': sources,
            'amount': income_amount,
            'description': income_description,
            'source': income_source,
            'date': income_date
        }

        if not income_amount:
            messages.error(request, 'Amount is required.')
            return render(request, 'incomes/income-edit.html', context)

        if not income_description:
            messages.error(request, 'Description is required.')
            return render(request, 'incomes/income-edit.html', context)

        income.amount=income_amount
        income.description=income_description
        income.source=income_source
        income.date=income_date
        income.save()

        messages.success(request, 'Income updated successfully.')
        return redirect('income')

    else:
        return render(request, 'income/income-edit.html', context)

@login_required(login_url='/authentication/login')
def income_delete(request, income_id):
    income = Income.objects.get(id=income_id)
    income.delete()
    messages.success(request, 'Income has been deleted.')
    return redirect('income')