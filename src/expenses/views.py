from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages

# Create your views here.

@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    return render(request, 'expenses/index.html')

def add_expense(request):
    categories = Category.objects.all()

    context = {
        'categories': categories
    }

    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)

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
            return render(request, 'expenses/add_expense.html', context)

        if not expense_description:
            messages.error(request, 'Description is required.')
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(
            owner=request.user,
            amount=expense_amount, 
            description=expense_description, 
            category=expense_category, 
            date=expense_date)

        messages.success(request, 'Expense saved successfully.')

        return redirect('expenses')