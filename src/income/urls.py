from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='income'),
    path('income-add', views.income_add, name='income-add'),
    path('income-edit/<str:pk>', views.income_edit, name='income-edit'),
    path('income-delete/<str:income_id>', views.income_delete, name='income-delete'),
    path('income-search', csrf_exempt(views.search_income), name='income-search'),
]
