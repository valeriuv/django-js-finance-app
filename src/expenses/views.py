from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from userpreferences.models import UserPreference
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse

# Create your views here.
def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = expenses.values()    # returns a list from QuerySet
        return JsonResponse(list(data), safe=False)

@login_required(login_url='/authentication/login')
def index(request):
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    currency_iso = currency.split()[0]

    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency,
        'currency_iso': currency_iso,
    }
    return render(request, 'expenses/index.html', context)

@login_required(login_url='/authentication/login')
def expense_add(request):
    categories = Category.objects.all()

    context = {
        'categories': categories
    }

    if request.method == 'GET':
        return render(request, 'expenses/expense-add.html', context)

    elif request.method == 'POST':

        expense_amount = request.POST['expense-amount'] # should map to the name of the input
        expense_description = request.POST['expense-description'] # should map to the name of the input
        expense_category = request.POST['expense-category'] # should map to the name of the input
        expense_date = request.POST['expense-date']
        
        context = {
            'categories': categories,
            'amount': expense_amount,
            'description': expense_description,
            'category': expense_category,
            'date': expense_date
        }

        if not expense_amount:
            messages.error(request, 'Amount is required.')
            return render(request, 'expenses/expense-add.html', context)

        if not expense_description:
            messages.error(request, 'Description is required.')
            return render(request, 'expenses/expense-add.html', context)

        if not expense_date:
            messages.error(request, 'Date of expense is required.')
            return render(request, 'expenses/expense-add.html', context)

        Expense.objects.create(
            owner=request.user,
            amount=expense_amount, 
            description=expense_description, 
            category=expense_category, 
            date=expense_date)

        messages.success(request, 'Expense saved successfully.')

        return redirect('expenses')

@login_required(login_url='/authentication/login')
def expense_edit(request, pk):
    expense = Expense.objects.get(id=pk)
    categories = Category.objects.exclude(name=expense.category)

    context = {
        'amount': expense.amount,
        'description': expense.description,
        'category': expense.category,
        'date': str(expense.date),
        'categories': categories,
        'expense_id': expense.id
    }

    if request.method == 'POST':

        expense_amount = request.POST['expense-amount'] # should map to the name of the input
        expense_description = request.POST['expense-description'] # should map to the name of the input
        expense_category = request.POST['expense-category'] # should map to the name of the input
        expense_date = request.POST['expense-date']
        
        context = {
            'categories': categories,
            'amount': expense_amount,
            'description': expense_description,
            'category': expense_category,
            'date': expense_date
        }

        if not expense_amount:
            messages.error(request, 'Amount is required.')
            return render(request, 'expenses/expense-edit.html', context)

        if not expense_description:
            messages.error(request, 'Description is required.')
            return render(request, 'expenses/expense-edit.html', context)

        expense.owner=request.user
        expense.amount=expense_amount
        expense.description=expense_description
        expense.category=expense_category
        expense.date=expense_date
        expense.save()

        messages.success(request, 'Expense updated successfully.')
        return redirect('expenses')

    else:
        return render(request, 'expenses/expense-edit.html', context)

@login_required(login_url='/authentication/login')
def expense_delete(request, expense_id):
    expense = Expense.objects.get(id=expense_id)
    print(expense)
    expense.delete()
    messages.success(request, 'Expense has been deleted.')
    return redirect('expenses')