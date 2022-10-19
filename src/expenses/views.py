from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from userpreferences.models import UserPreference
from django.contrib import messages
from django.core.paginator import Paginator
import json
import datetime
import csv
import xlwt
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum


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


def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=180)
    expenses = Expense.objects.filter(owner=request.user, date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}

    def get_category(expense):
        return expense.category

    category_list = list(set(map(get_category, expenses))) # call the function get_category on each expense in expenses

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)
        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y]=get_expense_category_amount(y)
    
    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def stats(request):
    return render(request, 'expenses/stats.html')


def export_csv(request):
    print(request.body)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=Expenses' + str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Category', 'Date'])

    expenses = Expense.objects.filter(owner=request.user)

    for expense in expenses:
        writer.writerow([expense.amount, expense.description, expense.category, expense.date])
    
    return response

def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; filename=Expenses' + str(datetime.datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount', 'Description', 'Category', 'Date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = Expense.objects.filter(owner=request.user).values_list('amount', 'description', 'category', 'date')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response


def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='inline; attachment; filename=Expenses' + str(datetime.datetime.now()) + '.pdf'
    response['Content-Transfer-Encoding'] = "binary"

    expenses = Expense.objects.filter(owner=request.user)
    sum = expenses.aggregate(Sum('amount'))

    html_string = render_to_string('expenses/pdf-output.html', {'expenses': expenses, 'total': sum['amount__sum']})

    html = HTML(string=html_string, base_url=request.build_absolute_uri())

    result = html.write_pdf(presentational_hints=True)

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')

        response.write(output.read())
    
    return response



