from django.urls import path, include
from . views import index, income, income_update, expenditure, lend_and_borrow, item_line, trip_line, income_source


app_name = 'main'


urlpatterns = [
    path('', index, name='index'),
    path('income/', income, name='income'),
    path('income/update/<int:pk>/', income_update, name='income-update'),
    path('expenditure/', expenditure, name='expenditure'),
    path('lend-and-borrow/', lend_and_borrow, name='lend-and-borrow'),
    path('item-line/', item_line, name='item-line'),
    path('trip-line/', trip_line, name='trip-line'),
    path('income-source/', income_source, name='income-source'),

]
