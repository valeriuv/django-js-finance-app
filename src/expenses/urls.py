from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='expenses'),
    path('expense-add', views.expense_add, name='expense-add'),
    path('expense-edit/<str:pk>', views.expense_edit, name='expense-edit'),
    path('expense-delete/<str:expense_id>', views.expense_delete, name='expense-delete'),
    path('expense-search', csrf_exempt(views.search_expenses), name='expense-search'),
]
