from django.urls import path, include
from . views import (
        index, income,
        income_update, 
        expenditure, 
        expenditure_update, 
        money_lended, 
        money_lended_update,
        money_borrowed, 
        item_line,
        trip_line, 
        income_source,
        money_borrowed_update,
    )

app_name = 'main'


urlpatterns = [
    path('', index, name='index'),
    path('income/', income, name='income'),
    path('income/update/<int:pk>/', income_update, name='income-update'),
    path('expenditure/', expenditure, name='expenditure'),
    path('expenditure/update/<int:pk>/', expenditure_update, name='expenditure-update'),
    path('money-lended/', money_lended, name='money-lended'),
    path('money-lended/update/<int:pk>/', money_lended_update, name='money-lended-update'),
    path('money-borrowed/', money_borrowed, name='money-borrowed'),
    path('money-borrowed/update/<int:pk>/', money_borrowed_update, name='money-borrowed-update'),
    path('item-line/', item_line, name='item-line'),
    path('trip-line/', trip_line, name='trip-line'),
    path('income-source/', income_source, name='income-source'),
]