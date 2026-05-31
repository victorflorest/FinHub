TRANSLATIONS = {
    'en': {
        'account_card': 'Account / Card',
        'actions': 'Actions',
        'add': 'Add',
        'add_transaction': 'Add Transaction',
        'all_categories': 'All Categories',
        'all_types': 'All Types',
        'amount': 'Amount',
        'balance': 'Balance',
        'cancel': 'Cancel',
        'category': 'Category',
        'credit_available': 'Available',
        'credit_used': 'Used',
        'dashboard': 'Dashboard',
        'date': 'Date',
        'dark': 'Dark',
        'delete': 'Delete',
        'delete_account': 'Delete Account',
        'delete_transaction': 'Delete Transaction',
        'description': 'Description',
        'edit': 'Edit',
        'expense': 'Expense',
        'expenses': 'Expenses',
        'export_excel': 'Export Excel',
        'filter': 'Filter',
        'financial_account': 'Financial Account',
        'financial_dashboard': 'Financial Dashboard',
        'financial_overview': 'Financial Overview',
        'income': 'Income',
        'language': 'Language',
        'light': 'Light',
        'login': 'Login',
        'logout': 'Logout',
        'no_transactions': 'No transactions found.',
        'recent_transactions': 'Recent Transactions',
        'register': 'Register',
        'save_account': 'Save Account',
        'save_transaction': 'Save Transaction',
        'search_description': 'Search description...',
        'theme': 'Theme',
        'total_expenses': 'Total Expenses',
        'total_income': 'Total Income',
        'transactions': 'Transactions',
        'type': 'Type',
        'update_transaction': 'Update Transaction',
    },
    'es': {
        'account_card': 'Cuenta / Tarjeta',
        'actions': 'Acciones',
        'add': 'Agregar',
        'add_transaction': 'Agregar Transaccion',
        'all_categories': 'Todas las categorias',
        'all_types': 'Todos los tipos',
        'amount': 'Monto',
        'balance': 'Balance',
        'cancel': 'Cancelar',
        'category': 'Categoria',
        'credit_available': 'Disponible',
        'credit_used': 'Usado',
        'dashboard': 'Panel',
        'date': 'Fecha',
        'dark': 'Oscuro',
        'delete': 'Eliminar',
        'delete_account': 'Eliminar cuenta',
        'delete_transaction': 'Eliminar transaccion',
        'description': 'Descripcion',
        'edit': 'Editar',
        'expense': 'Gasto',
        'expenses': 'Gastos',
        'export_excel': 'Exportar Excel',
        'filter': 'Filtrar',
        'financial_account': 'Cuenta financiera',
        'financial_dashboard': 'Panel financiero',
        'financial_overview': 'Resumen financiero',
        'income': 'Ingreso',
        'language': 'Idioma',
        'light': 'Claro',
        'login': 'Ingresar',
        'logout': 'Salir',
        'no_transactions': 'No se encontraron transacciones.',
        'recent_transactions': 'Transacciones recientes',
        'register': 'Registrarse',
        'save_account': 'Guardar cuenta',
        'save_transaction': 'Guardar transaccion',
        'search_description': 'Buscar descripcion...',
        'theme': 'Tema',
        'total_expenses': 'Total gastos',
        'total_income': 'Total ingresos',
        'transactions': 'Transacciones',
        'type': 'Tipo',
        'update_transaction': 'Actualizar transaccion',
    },
}


ACCOUNT_TYPE_LABELS = {
    'en': {
        'cash': 'Cash',
        'debit_card': 'Debit Card',
        'credit_card': 'Credit Card',
    },
    'es': {
        'cash': 'Efectivo',
        'debit_card': 'Debito',
        'credit_card': 'Credito',
    },
}


CATEGORY_LABELS = {
    'en': {
        'Ingresos': 'Income',
        'Sueldo': 'Salary',
        'Salario': 'Salary',
        'Alimentacion': 'Food',
        'Transporte': 'Transport',
        'Hogar y servicios': 'Home & utilities',
        'Salud': 'Health',
        'Educacion': 'Education',
        'Entretenimiento': 'Entertainment',
        'Otros': 'Other',
        'Initial Balance': 'Initial balance',
    },
    'es': {
        'Ingresos': 'Ingresos',
        'Sueldo': 'Sueldo',
        'Salario': 'Sueldo',
        'Alimentacion': 'Alimentacion',
        'Transporte': 'Transporte',
        'Hogar y servicios': 'Hogar y servicios',
        'Salud': 'Salud',
        'Educacion': 'Educacion',
        'Entretenimiento': 'Entretenimiento',
        'Otros': 'Otros',
        'Initial Balance': 'Saldo inicial',
    },
}


def translate_category_name(name, language):
    return CATEGORY_LABELS.get(language, CATEGORY_LABELS['es']).get(name, name)


def get_language(request):
    if request.user.is_authenticated:
        return request.user.ui_language

    return request.session.get(
        'ui_language',
        request.COOKIES.get('ui_language', 'es')
    )


def get_theme(request):
    if request.user.is_authenticated:
        return request.user.ui_theme

    return request.session.get(
        'ui_theme',
        request.COOKIES.get('ui_theme', 'dark')
    )
