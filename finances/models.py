from django.conf import settings
from django.db import models
from django.db import transaction as db_transaction


class FinancialAccount(models.Model):

    ACCOUNT_TYPES = [
        ('cash', 'Cash'),
        ('debit_card', 'Debit Card'),
        ('credit_card', 'Credit Card'),
    ]

    CURRENCIES = [
        ('PEN', 'Soles'),
        ('USD', 'Dollars'),
        ('EUR', 'Euro'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='accounts'
    )

    name = models.CharField(
        max_length=100
    )

    bank_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPES
    )

    currency = models.CharField(
        max_length=10,
        choices=CURRENCIES,
        default='PEN'
    )

    current_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    used_credit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    credit_limit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )

    statement_closing_day = models.IntegerField(
        blank=True,
        null=True
    )

    payment_due_day = models.IntegerField(
        blank=True,
        null=True
    )

    account_number = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    cci = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    color = models.CharField(
        max_length=7,
        default='#000000'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    @property
    def available_credit(self):
        limit = self.credit_limit if self.credit_limit is not None else self.current_balance
        return limit - self.used_credit

    @property
    def display_account_type(self):
        legacy_debit_types = ['bank', 'digital_wallet', 'crypto']

        if self.account_type in legacy_debit_types:
            return 'Debit Card'

        return self.get_account_type_display()

    def __str__(self):
        return self.name


class Category(models.Model):

    CATEGORY_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    name = models.CharField(
        max_length=100,
        unique=True
    )

    category_type = models.CharField(
        max_length=10,
        choices=CATEGORY_TYPES
    )

    color = models.CharField(
        max_length=7,
        default='#000000'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


class Transaction(models.Model):

    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions'
    )

    account = models.ForeignKey(
        FinancialAccount,
        on_delete=models.CASCADE,
        related_name='transactions',
        null=True,
        blank=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='transactions'
    )

    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    transaction_date = models.DateField(
        auto_now_add=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def _apply_to_account(self):
        if not self.account:
            return

        if self.account.account_type == 'credit_card':
            if self.transaction_type == 'expense':
                self.account.used_credit += self.amount
            elif self.transaction_type == 'income':
                self.account.used_credit -= self.amount
                if self.account.used_credit < 0:
                    self.account.used_credit = 0
        else:
            if self.transaction_type == 'expense':
                self.account.current_balance -= self.amount
            elif self.transaction_type == 'income':
                self.account.current_balance += self.amount

        self.account.save()

    def _reverse_from_account(self):
        if not self.account:
            return

        if self.account.account_type == 'credit_card':
            if self.transaction_type == 'expense':
                self.account.used_credit -= self.amount
                if self.account.used_credit < 0:
                    self.account.used_credit = 0
            elif self.transaction_type == 'income':
                self.account.used_credit += self.amount
        else:
            if self.transaction_type == 'expense':
                self.account.current_balance += self.amount
            elif self.transaction_type == 'income':
                self.account.current_balance -= self.amount

        self.account.save()

    def save(self, *args, **kwargs):
        with db_transaction.atomic():
            old_transaction = None

            if self.pk:
                old_transaction = (
                    Transaction.objects
                    .select_related('account')
                    .get(pk=self.pk)
                )

            super().save(*args, **kwargs)

            if old_transaction:
                old_transaction._reverse_from_account()

            if self.account:
                self.account.refresh_from_db()

            self._apply_to_account()

    def delete(self, *args, **kwargs):
        with db_transaction.atomic():
            self._reverse_from_account()
            return super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} - {self.amount}'
