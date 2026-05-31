from django.db import migrations, models


def map_legacy_account_types(apps, schema_editor):
    FinancialAccount = apps.get_model('finances', 'FinancialAccount')

    FinancialAccount.objects.filter(
        account_type__in=['bank', 'digital_wallet', 'crypto']
    ).update(account_type='debit_card')


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0004_financialaccount_used_credit'),
    ]

    operations = [
        migrations.RunPython(
            map_legacy_account_types,
            migrations.RunPython.noop
        ),
        migrations.AlterField(
            model_name='financialaccount',
            name='account_type',
            field=models.CharField(
                choices=[
                    ('cash', 'Cash'),
                    ('debit_card', 'Debit Card'),
                    ('credit_card', 'Credit Card'),
                ],
                max_length=20
            ),
        ),
    ]
