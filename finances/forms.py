from django import forms
from .models import Transaction, FinancialAccount
from .preferences import ACCOUNT_TYPE_LABELS, TRANSLATIONS, translate_category_name


class TransactionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user', None)
        language = kwargs.pop('language', 'es')

        super().__init__(*args, **kwargs)
        labels = TRANSLATIONS[language]

        if user:

            self.fields['account'].queryset = (
                FinancialAccount.objects.filter(
                    user=user
                )
            )

        self.fields['account'].label = labels['account_card']
        self.fields['category'].label = labels['category']
        self.fields['transaction_type'].label = labels['type']
        self.fields['amount'].label = labels['amount']
        self.fields['description'].label = labels['description']
        self.fields['transaction_type'].choices = [
            ('income', labels['income']),
            ('expense', labels['expense']),
        ]
        self.fields['category'].label_from_instance = (
            lambda category: translate_category_name(category.name, language)
        )

    class Meta:

        model = Transaction

        fields = [

            'account',
            'category',
            'transaction_type',
            'amount',
            'description',
        ]

        widgets = {

            'account': forms.Select(attrs={
                'class': 'form-control'
            }),

            'category': forms.Select(attrs={
                'class': 'form-control'
            }),

            'transaction_type': forms.Select(attrs={
                'class': 'form-control'
            }),

            'amount': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }

class FinancialAccountForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        language = kwargs.pop('language', 'es')
        super().__init__(*args, **kwargs)
        account_labels = ACCOUNT_TYPE_LABELS[language]
        self.fields['account_type'].choices = [
            ('cash', account_labels['cash']),
            ('debit_card', account_labels['debit_card']),
            ('credit_card', account_labels['credit_card']),
        ]
        self.fields['current_balance'].required = False
        self.fields['credit_limit'].required = False
        self.fields['statement_closing_day'].required = False
        self.fields['payment_due_day'].required = False
        self.fields['name'].label = 'Nombre' if language == 'es' else 'Name'
        self.fields['bank_name'].label = 'Banco' if language == 'es' else 'Bank name'
        self.fields['account_type'].label = 'Tipo de cuenta' if language == 'es' else 'Account type'
        self.fields['currency'].label = 'Moneda' if language == 'es' else 'Currency'
        self.fields['current_balance'].label = 'Saldo inicial' if language == 'es' else 'Initial balance'
        self.fields['credit_limit'].label = 'Linea de credito' if language == 'es' else 'Credit limit'
        self.fields['statement_closing_day'].label = 'Dia de facturacion' if language == 'es' else 'Statement closing day'
        self.fields['payment_due_day'].label = 'Dia de pago' if language == 'es' else 'Payment due day'
        self.fields['account_number'].label = 'Numero de cuenta' if language == 'es' else 'Account number'
        self.fields['cci'].label = 'CCI'
        self.fields['color'].label = 'Color'

        if not self.instance.pk:
            self.fields['account_type'].initial = 'debit_card'

    def clean(self):
        cleaned_data = super().clean()
        account_type = cleaned_data.get('account_type')

        if account_type == 'credit_card':
            cleaned_data['current_balance'] = 0

            for field in ('credit_limit', 'statement_closing_day', 'payment_due_day'):
                if not cleaned_data.get(field):
                    self.add_error(field, 'This field is required for credit cards.')
        elif cleaned_data.get('current_balance') is None:
            cleaned_data['current_balance'] = 0
        else:
            cleaned_data['credit_limit'] = None
            cleaned_data['statement_closing_day'] = None
            cleaned_data['payment_due_day'] = None

        return cleaned_data

    class Meta:

        model = FinancialAccount

        fields = [

            'name',
            'bank_name',
            'account_type',
            'currency',
            'current_balance',
            'credit_limit',
            'statement_closing_day',
            'payment_due_day',
            'account_number',
            'cci',
            'color',
        ]

        widgets = {

            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'bank_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'account_type': forms.Select(attrs={
                'class': 'form-control',
                'data-account-type': 'true'
            }),

            'currency': forms.Select(attrs={
                'class': 'form-control'
            }),

            'current_balance': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'data-balance-field': 'true'
            }),

            'credit_limit': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'data-credit-field': 'true'
            }),

            'statement_closing_day': forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1,
            'max': 31,
            'data-credit-field': 'true'
            }),

            'payment_due_day': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 31,
                'data-credit-field': 'true'
            }),

            'account_number': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'cci': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color'
            }),
        }

