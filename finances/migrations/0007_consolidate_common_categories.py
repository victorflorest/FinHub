from django.db import migrations


TARGET_CATEGORIES = [
    ('Ingresos', 'income', '#16a34a'),
    ('Alimentacion', 'expense', '#ef4444'),
    ('Transporte', 'expense', '#f97316'),
    ('Hogar y servicios', 'expense', '#6366f1'),
    ('Salud', 'expense', '#ec4899'),
    ('Educacion', 'expense', '#3b82f6'),
    ('Entretenimiento', 'expense', '#a855f7'),
    ('Otros', 'expense', '#6b7280'),
]


CATEGORY_MAPPING = {
    'Salario': 'Ingresos',
    'Freelance': 'Ingresos',
    'Bonos': 'Ingresos',
    'Intereses': 'Ingresos',
    'Reembolsos': 'Ingresos',
    'Ventas': 'Ingresos',
    'Initial Balance': 'Ingresos',
    'Alimentacion': 'Alimentacion',
    'Restaurantes': 'Alimentacion',
    'Supermercado': 'Alimentacion',
    'Transporte': 'Transporte',
    'Vivienda': 'Hogar y servicios',
    'Servicios': 'Hogar y servicios',
    'Salud': 'Salud',
    'Educacion': 'Educacion',
    'Entretenimiento': 'Entretenimiento',
    'Suscripciones': 'Entretenimiento',
    'Compras': 'Otros',
    'Viajes': 'Otros',
    'Mascotas': 'Otros',
    'Seguros': 'Otros',
    'Impuestos': 'Otros',
    'Pago de tarjeta': 'Otros',
    'Transferencias': 'Otros',
    'Otros': 'Otros',
}


def consolidate_categories(apps, schema_editor):
    Category = apps.get_model('finances', 'Category')
    Transaction = apps.get_model('finances', 'Transaction')

    target_categories = {}

    for name, category_type, color in TARGET_CATEGORIES:
        category, _ = Category.objects.get_or_create(
            name=name,
            defaults={
                'category_type': category_type,
                'color': color,
            }
        )

        updates = {}

        if category.category_type != category_type:
            updates['category_type'] = category_type

        if category.color == '#000000':
            updates['color'] = color

        if updates:
            for field, value in updates.items():
                setattr(category, field, value)

            category.save(update_fields=list(updates.keys()))

        target_categories[name] = category

    for source_name, target_name in CATEGORY_MAPPING.items():
        try:
            source_category = Category.objects.get(name=source_name)
        except Category.DoesNotExist:
            continue

        target_category = target_categories[target_name]

        if source_category.pk != target_category.pk:
            Transaction.objects.filter(
                category=source_category
            ).update(category=target_category)

            source_category.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0006_seed_common_categories'),
    ]

    operations = [
        migrations.RunPython(
            consolidate_categories,
            migrations.RunPython.noop
        ),
    ]
