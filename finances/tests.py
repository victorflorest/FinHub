from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import FinancialAccountForm
from .models import Category, FinancialAccount, Transaction
from .preferences import get_language, get_theme, translate_category_name


class TransactionBalanceTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='tester',
            password='password123'
        )
        self.expense_category = Category.objects.create(
            name='Food',
            category_type='expense'
        )
        self.income_category = Category.objects.create(
            name='Payment',
            category_type='income'
        )

    def test_expense_decreases_normal_account_balance(self):
        account = FinancialAccount.objects.create(
            user=self.user,
            name='Cash',
            account_type='cash',
            current_balance=Decimal('100.00')
        )

        Transaction.objects.create(
            user=self.user,
            account=account,
            category=self.expense_category,
            transaction_type='expense',
            amount=Decimal('25.00')
        )

        account.refresh_from_db()
        self.assertEqual(account.current_balance, Decimal('75.00'))

    def test_credit_card_expense_increases_used_credit(self):
        account = FinancialAccount.objects.create(
            user=self.user,
            name='Visa',
            account_type='credit_card',
            credit_limit=Decimal('1000.00')
        )

        Transaction.objects.create(
            user=self.user,
            account=account,
            category=self.expense_category,
            transaction_type='expense',
            amount=Decimal('120.00')
        )

        account.refresh_from_db()
        self.assertEqual(account.used_credit, Decimal('120.00'))
        self.assertEqual(account.available_credit, Decimal('880.00'))

    def test_credit_card_income_decreases_used_credit(self):
        account = FinancialAccount.objects.create(
            user=self.user,
            name='Visa',
            account_type='credit_card',
            used_credit=Decimal('120.00'),
            credit_limit=Decimal('1000.00')
        )

        Transaction.objects.create(
            user=self.user,
            account=account,
            category=self.income_category,
            transaction_type='income',
            amount=Decimal('50.00')
        )

        account.refresh_from_db()
        self.assertEqual(account.used_credit, Decimal('70.00'))

    def test_updating_transaction_recalculates_account_balance(self):
        account = FinancialAccount.objects.create(
            user=self.user,
            name='Cash',
            account_type='cash',
            current_balance=Decimal('100.00')
        )
        transaction = Transaction.objects.create(
            user=self.user,
            account=account,
            category=self.expense_category,
            transaction_type='expense',
            amount=Decimal('25.00')
        )

        transaction.amount = Decimal('40.00')
        transaction.save()

        account.refresh_from_db()
        self.assertEqual(account.current_balance, Decimal('60.00'))

    def test_deleting_transaction_reverses_account_balance(self):
        account = FinancialAccount.objects.create(
            user=self.user,
            name='Cash',
            account_type='cash',
            current_balance=Decimal('100.00')
        )
        transaction = Transaction.objects.create(
            user=self.user,
            account=account,
            category=self.expense_category,
            transaction_type='expense',
            amount=Decimal('25.00')
        )

        transaction.delete()

        account.refresh_from_db()
        self.assertEqual(account.current_balance, Decimal('100.00'))

    def test_account_initial_balance_is_created_as_income_transaction(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('account_create'), {
            'name': 'Debit',
            'bank_name': 'Demo Bank',
            'account_type': 'debit_card',
            'currency': 'PEN',
            'current_balance': '250.00',
            'account_number': '',
            'cci': '',
            'color': '#333333',
        })

        self.assertEqual(response.status_code, 302)

        account = FinancialAccount.objects.get(name='Debit')
        transaction = Transaction.objects.get(
            account=account,
            transaction_type='income'
        )

        account.refresh_from_db()
        self.assertEqual(account.current_balance, Decimal('250.00'))
        self.assertEqual(transaction.amount, Decimal('250.00'))
        self.assertEqual(transaction.category.name, 'Initial Balance')

    def test_credit_card_requires_billing_and_payment_dates(self):
        form = FinancialAccountForm(data={
            'name': 'Credit',
            'account_type': 'credit_card',
            'currency': 'PEN',
            'current_balance': '0.00',
            'credit_limit': '1000.00',
            'account_number': '',
            'cci': '',
            'color': '#333333',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('statement_closing_day', form.errors)
        self.assertIn('payment_due_day', form.errors)

    def test_credit_card_can_be_created_without_current_balance(self):
        form = FinancialAccountForm(data={
            'name': 'Credit',
            'account_type': 'credit_card',
            'currency': 'PEN',
            'credit_limit': '1000.00',
            'statement_closing_day': '15',
            'payment_due_day': '28',
            'account_number': '',
            'cci': '',
            'color': '#333333',
        })

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['current_balance'], 0)

    def test_preferences_are_saved_in_cookies(self):
        response = self.client.get(
            reverse('set_preferences'),
            {'language': 'en', 'theme': 'light', 'next': '/dashboard/'}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.cookies['ui_language'].value, 'en')
        self.assertEqual(response.cookies['ui_theme'].value, 'light')

    def test_preferences_fall_back_to_cookies(self):
        request = type('Request', (), {
            'user': type('AnonymousUser', (), {'is_authenticated': False})(),
            'session': {},
            'COOKIES': {
                'ui_language': 'en',
                'ui_theme': 'light',
            },
        })()

        self.assertEqual(get_language(request), 'en')
        self.assertEqual(get_theme(request), 'light')

    def test_authenticated_user_preferences_override_cookies(self):
        self.user.ui_language = 'es'
        self.user.ui_theme = 'dark'
        self.user.save(update_fields=['ui_language', 'ui_theme'])

        request = type('Request', (), {
            'user': self.user,
            'session': {},
            'COOKIES': {
                'ui_language': 'en',
                'ui_theme': 'light',
            },
        })()

        self.assertEqual(get_language(request), 'es')
        self.assertEqual(get_theme(request), 'dark')

    def test_authenticated_preference_change_is_saved_to_user(self):
        self.client.force_login(self.user)

        self.client.get(
            reverse('set_preferences'),
            {'language': 'en', 'theme': 'light', 'next': '/dashboard/'}
        )

        self.user.refresh_from_db()
        self.assertEqual(self.user.ui_language, 'en')
        self.assertEqual(self.user.ui_theme, 'light')

    def test_common_categories_are_available(self):
        expected_categories = [
            'Ingresos',
            'Alimentacion',
            'Transporte',
            'Hogar y servicios',
            'Salud',
            'Educacion',
            'Entretenimiento',
            'Otros',
        ]

        existing_categories = set(
            Category.objects.filter(
                name__in=expected_categories
            ).values_list('name', flat=True)
        )

        self.assertEqual(existing_categories, set(expected_categories))

    def test_category_names_can_be_translated_for_display(self):
        self.assertEqual(
            translate_category_name('Alimentacion', 'en'),
            'Food'
        )
        self.assertEqual(
            translate_category_name('Alimentacion', 'es'),
            'Alimentacion'
        )
        self.assertEqual(
            translate_category_name('Sueldo', 'en'),
            'Salary'
        )
