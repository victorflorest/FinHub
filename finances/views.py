from django.shortcuts import render,redirect
from .models import Transaction, Category
from .forms import TransactionForm, FinancialAccountForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import openpyxl
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TransactionSerializer
from .models import FinancialAccount
from decimal import Decimal
from .preferences import get_language, translate_category_name

def home(request):
    return redirect('dashboard')


def set_preferences(request):
    language = request.GET.get('language')
    theme = request.GET.get('theme')
    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER') or 'dashboard'
    response = redirect(next_url)

    if language in ('en', 'es'):
        request.session['ui_language'] = language

        if request.user.is_authenticated:
            request.user.ui_language = language
            request.user.save(update_fields=['ui_language'])

        response.set_cookie(
            'ui_language',
            language,
            max_age=60 * 60 * 24 * 365,
            samesite='Lax'
        )

    if theme in ('dark', 'light'):
        request.session['ui_theme'] = theme

        if request.user.is_authenticated:
            request.user.ui_theme = theme
            request.user.save(update_fields=['ui_theme'])

        response.set_cookie(
            'ui_theme',
            theme,
            max_age=60 * 60 * 24 * 365,
            samesite='Lax'
        )

    return response

@login_required
def transaction_list(request):
    language = get_language(request)

    transactions = Transaction.objects.filter(
        user=request.user
    ).select_related('account', 'category')

    search_query = request.GET.get('search')

    transaction_type = request.GET.get('type')

    category = request.GET.get('category')

    if search_query:

        transactions = transactions.filter(
            description__icontains=search_query
        )

    if transaction_type:

        transactions = transactions.filter(
            transaction_type=transaction_type
        )

    if category:

        transactions = transactions.filter(
            category__id=category
        )

    categories = list(Category.objects.all())

    for category_item in categories:
        category_item.display_name = translate_category_name(
            category_item.name,
            language
        )

    transactions = list(transactions.order_by(
        '-transaction_date'
    ))

    for transaction in transactions:
        transaction.display_category_name = translate_category_name(
            transaction.category.name,
            language
        ) if transaction.category else '-'

    context = {

        'transactions': transactions,

        'categories': categories,
    }

    return render(
        request,
        'finances/transaction_list.html',
        context
    )

@login_required
def transaction_create(request):

    if request.method == 'POST':

        form = TransactionForm(
            request.POST,
            user=request.user,
            language=get_language(request)
        )

        if form.is_valid():

            transaction = form.save(commit=False)

            transaction.user = request.user

            transaction.save()

            return redirect('transaction_list')

    else:

        form = TransactionForm(
            user=request.user,
            language=get_language(request)
        )

    return render(
        request,
        'finances/transaction_create.html',
        {'form': form}
    )

@login_required
def transaction_update(request, pk):

    transaction = get_object_or_404(
        Transaction,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':

        form = TransactionForm(
            request.POST,
            instance=transaction,
            user=request.user,
            language=get_language(request)
        )

        if form.is_valid():

            form.save()

            return redirect('transaction_list')

    else:

        form = TransactionForm(
            instance=transaction,
            user=request.user,
            language=get_language(request)
        )

    return render(
        request,
        'finances/transaction_update.html',
        {'form': form}
    )

@login_required
def transaction_delete(request, pk):

    transaction = get_object_or_404(
        Transaction,
        pk=pk
    )

    if request.method == 'POST':

        transaction.delete()

        return redirect('transaction_list')

    context = {
        'transaction': transaction
    }

    return render(
        request,
        'finances/transaction_delete.html',
        context
    )

@login_required
def dashboard(request):
    language = get_language(request)

    income_total = Transaction.objects.filter(
        user=request.user,
        transaction_type='income'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    expense_total = Transaction.objects.filter(
        user=request.user,
        transaction_type='expense'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    balance = income_total - expense_total
    chart_total = income_total + expense_total

    if chart_total:
        income_degrees = round(float(income_total / chart_total * 360), 2)
        expense_degrees = 360 - income_degrees
    else:
        income_degrees = 0
        expense_degrees = 0

    recent_transactions = list(Transaction.objects.filter(
        user=request.user
    ).select_related('account', 'category').order_by('-transaction_date')[:5])

    for transaction in recent_transactions:
        transaction.display_category_name = translate_category_name(
            transaction.category.name,
            language
        ) if transaction.category else '-'

    accounts = FinancialAccount.objects.filter(
        user=request.user
    )

    context = {

        'income_total': income_total,
        'expense_total': expense_total,
        'balance': balance,
        'recent_transactions': recent_transactions,
        'income_chart': float(income_total),
        'expense_chart': float(expense_total),
        'income_degrees': income_degrees,
        'expense_degrees': expense_degrees,
        'has_chart_data': chart_total > 0,
        'accounts': accounts,
    }

    return render(
        request,
        'finances/dashboard.html',
        context
    )

@login_required
def export_transactions_excel(request):

    transactions = Transaction.objects.filter(
        user=request.user
    ).select_related('account', 'category')

    workbook = openpyxl.Workbook()

    worksheet = workbook.active

    worksheet.title = 'Transactions'

    headers = [
        'Category',
        'Type',
        'Amount',
        'Account',
        'Date',
        'Description'
    ]

    worksheet.append(headers)

    for transaction in transactions:

        worksheet.append([

            str(transaction.category),

            transaction.transaction_type,

            float(transaction.amount),

            str(transaction.account) if transaction.account else '',

            str(transaction.transaction_date),

            transaction.description,
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response['Content-Disposition'] = (
        'attachment; filename=transactions.xlsx'
    )

    workbook.save(response)

    return response

@api_view(['GET'])
def transactions_api(request):

    transactions = Transaction.objects.filter(
        user=request.user
    ).select_related('account', 'category')

    serializer = TransactionSerializer(
        transactions,
        many=True
    )

    return Response(serializer.data)


@login_required
def account_create(request):

    if request.method == 'POST':

        form = FinancialAccountForm(
            request.POST,
            language=get_language(request)
        )

        if form.is_valid():

            account = form.save(commit=False)
            account.user = request.user

            initial_balance = account.current_balance or Decimal('0.00')

            if account.account_type in ('cash', 'debit_card'):
                account.current_balance = Decimal('0.00')

            account.save()

            if account.account_type in ('cash', 'debit_card') and initial_balance > 0:
                category, _ = Category.objects.get_or_create(
                    name='Initial Balance',
                    defaults={'category_type': 'income'}
                )

                if category.category_type != 'income':
                    category.category_type = 'income'
                    category.save(update_fields=['category_type'])

                Transaction.objects.create(
                    user=request.user,
                    account=account,
                    category=category,
                    transaction_type='income',
                    amount=initial_balance,
                    description='Initial account balance'
                )

            return redirect('dashboard')

    else:

        form = FinancialAccountForm(
            language=get_language(request)
        )

    return render(
        request,
        'finances/account_form.html',
        {'form': form}
    )


@login_required
def account_update(request, pk):

    account = get_object_or_404(
        FinancialAccount,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':

        form = FinancialAccountForm(
            request.POST,
            instance=account,
            language=get_language(request)
        )

        if form.is_valid():

            form.save()

            return redirect('dashboard')

    else:

        form = FinancialAccountForm(
            instance=account,
            language=get_language(request)
        )

    return render(
        request,
        'finances/account_form.html',
        {'form': form}
    )


@login_required
def account_delete(request, pk):

    account = get_object_or_404(
        FinancialAccount,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':

        account.delete()

        return redirect('dashboard')

    return render(
        request,
        'finances/account_confirm_delete.html',
        {
            'account': account,
            'transaction_count': account.transactions.count()
        }
    )


