from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='expenses'),
    path('expense-add', views.expense_add, name='expense-add'),
    path('expense-edit/<str:pk>', views.expense_edit, name='expense-edit'),
    path('expense-delete/<str:expense_id>', views.expense_delete, name='expense-delete'),

]
