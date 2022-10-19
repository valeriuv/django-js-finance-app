from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='expenses'),
    path('expense-add', views.expense_add, name='expense-add'),
    path('expense-edit/<str:pk>', views.expense_edit, name='expense-edit'),
    path('expense-delete/<str:expense_id>', views.expense_delete, name='expense-delete'),
    path('expense-search', csrf_exempt(views.search_expenses), name='expense-search'),
    path('expense_category_summary', views.expense_category_summary, name='expense_category_summary'),
    path('stats', views.stats, name='stats'),
    path('export-csv', views.export_csv, name='export-csv'),
    path('export-excel', views.export_excel, name='export-excel'),
    path('export-pdf', views.export_pdf, name='export-pdf'), 
]
