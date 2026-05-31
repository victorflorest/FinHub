from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ui_language',
            field=models.CharField(
                choices=[
                    ('es', 'Spanish'),
                    ('en', 'English'),
                ],
                default='es',
                max_length=2
            ),
        ),
        migrations.AddField(
            model_name='user',
            name='ui_theme',
            field=models.CharField(
                choices=[
                    ('dark', 'Dark'),
                    ('light', 'Light'),
                ],
                default='dark',
                max_length=5
            ),
        ),
    ]
