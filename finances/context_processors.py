from .preferences import ACCOUNT_TYPE_LABELS, TRANSLATIONS, get_language, get_theme


def ui_preferences(request):
    language = get_language(request)
    theme = get_theme(request)

    return {
        'ui_language': language,
        'ui_theme': theme,
        't': TRANSLATIONS[language],
        'account_type_labels': ACCOUNT_TYPE_LABELS[language],
    }
