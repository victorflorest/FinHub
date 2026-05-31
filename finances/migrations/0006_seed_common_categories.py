from django.db import migrations


COMMON_CATEGORIES = [
    ('Salario', 'income', '#16a34a'),
    ('Freelance', 'income', '#22c55e'),
    ('Bonos', 'income', '#84cc16'),
    ('Intereses', 'income', '#14b8a6'),
    ('Reembolsos', 'income', '#06b6d4'),
    ('Ventas', 'income', '#0ea5e9'),
    ('Alimentacion', 'expense', '#ef4444'),
    ('Transporte', 'expense', '#f97316'),
    ('Vivienda', 'expense', '#8b5cf6'),
    ('Servicios', 'expense', '#6366f1'),
    ('Salud', 'expense', '#ec4899'),
    ('Educacion', 'expense', '#3b82f6'),
    ('Entretenimiento', 'expense', '#a855f7'),
    ('Compras', 'expense', '#f59e0b'),
    ('Restaurantes', 'expense', '#fb7185'),
    ('Supermercado', 'expense', '#dc2626'),
    ('Viajes', 'expense', '#0891b2'),
    ('Mascotas', 'expense', '#65a30d'),
    ('Seguros', 'expense', '#475569'),
    ('Impuestos', 'expense', '#64748b'),
    ('Pago de tarjeta', 'expense', '#7c3aed'),
    ('Transferencias', 'expense', '#2563eb'),
    ('Suscripciones', 'expense', '#db2777'),
    ('Otros', 'expense', '#6b7280'),
]


def seed_common_categories(apps, schema_editor):
    Category = apps.get_model('finances', 'Category')

    for name, category_type, color in COMMON_CATEGORIES:
        Category.objects.get_or_create(
            name=name,
            defaults={
                'category_type': category_type,
                'color': color,
            }
        )


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0005_simplify_account_types'),
    ]

    operations = [
        migrations.RunPython(
            seed_common_categories,
            migrations.RunPython.noop
        ),
    ]
