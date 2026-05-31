from django.urls import path
from .views import (
    home,
    dashboard,
    transaction_list,
    transaction_create,
    transaction_update,
    transaction_delete,
    export_transactions_excel,
    transactions_api,
    account_create,
    account_update,
    account_delete,
    set_preferences
)

urlpatterns = [
    path('', home, name='home'),

    path(
        'preferences/',
        set_preferences,
        name='set_preferences'
    ),

    path(
        'transactions/',
        transaction_list,
        name='transaction_list'
    ),

    path(
    'transactions/create/',
    transaction_create,
    name='transaction_create'
    ),
    path(
    'transactions/<int:pk>/update/',
    transaction_update,
    name='transaction_update'
    ),

    path(
        'transactions/<int:pk>/delete/',
        transaction_delete,
        name='transaction_delete'
    ),

    path(
    'dashboard/',
    dashboard,
    name='dashboard'
    ),
    
    path(
    'transactions/export/excel/',
    export_transactions_excel,
    name='export_transactions_excel'
    ),
    
    path(
    'api/transactions/',
    transactions_api,
    name='transactions_api'
    ),


    path(
        'accounts/create/',
        account_create,
        name='account_create'
    ),

    path(
        'accounts/<int:pk>/update/',
        account_update,
        name='account_update'
    ),

    path(
        'accounts/<int:pk>/delete/',
        account_delete,
        name='account_delete'
    ),

]
