# Deploying Financial Tracker

## Recommended Setup

Use Neon for PostgreSQL and Render for the Django web app.

## Required Environment Variables

Set these in your hosting provider:

```text
DATABASE_URL=your-neon-database-url
SECRET_KEY=generate-a-long-random-secret
DEBUG=False
ALLOWED_HOSTS=.onrender.com
CSRF_TRUSTED_ORIGINS=https://*.onrender.com
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
```

For a custom domain, replace `.onrender.com` and `https://*.onrender.com`
with your production domain.

## Render Commands

Build command:

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

Start command:

```bash
python manage.py migrate && gunicorn financialsite.wsgi:application --log-file -
```

## Important

Do not commit `.env`, `venv/`, `db.sqlite3`, or `staticfiles/`.
They are already listed in `.gitignore`.
