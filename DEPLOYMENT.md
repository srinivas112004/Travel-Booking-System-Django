# 🚀 Deployment Guide - Travel Booking System

Complete guide to deploy your Django application to production.

---

## 📋 Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Option 1: PythonAnywhere (Easiest - Free)](#option-1-pythonanywhere)
3. [Option 2: Render (Modern - Free Tier)](#option-2-render)
4. [Option 3: Railway (Simple - Free Trial)](#option-3-railway)
5. [Option 4: Heroku (Popular - Paid)](#option-4-heroku)
6. [Post-Deployment Steps](#post-deployment-steps)

---

## 🔍 Pre-Deployment Checklist

### 1. Update `settings.py` for Production

Create a `production_settings.py` or update existing settings:

```python
import os
from pathlib import Path

# Security Settings
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-production-secret-key')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'your-domain.com').split(',')

# HTTPS/Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static Files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# Media Files
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'
```

### 2. Create `requirements.txt` (Already done)

Verify it contains all dependencies:
```bash
pip freeze > requirements.txt
```

### 3. Create `runtime.txt`

Specify Python version:
```
python-3.10.0
```

### 4. Create `.env` file (Don't commit this!)

```env
SECRET_KEY=your-super-secret-key-here
DEBUG=0
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=your-database-url
```

---

## 🎯 Option 1: PythonAnywhere (Recommended for Beginners)

**Pros:** Free tier, Easy setup, No credit card required  
**Cons:** Limited resources on free tier  
**Free Tier:** 512 MB storage, 1 web app

### Step-by-Step Guide:

#### 1. Sign Up
- Go to [www.pythonanywhere.com](https://www.pythonanywhere.com)
- Create a free "Beginner" account

#### 2. Upload Your Code

**Option A: Via GitHub (Recommended)**
```bash
# In PythonAnywhere Bash Console
git clone https://github.com/srinivas112004/Travel-Booking-System-Django.git
cd Travel-Booking-System-Django
```

**Option B: Upload Files**
- Use PythonAnywhere's file upload feature
- Upload your project as a ZIP file

#### 3. Create Virtual Environment
```bash
# In PythonAnywhere Bash Console
mkvirtualenv --python=/usr/bin/python3.10 travel-env
workon travel-env
cd Travel-Booking-System-Django
pip install -r requirements.txt
```

#### 4. Configure Web App

Go to **Web** tab → **Add a new web app**:

1. Select **Manual configuration**
2. Choose **Python 3.10**

#### 5. Configure WSGI File

Click on WSGI configuration file and replace with:

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/YOUR_USERNAME/Travel-Booking-System-Django'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variable for Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'travel_booking.settings'

# Activate virtual environment
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

#### 6. Set Virtual Environment Path

In **Web** tab → **Virtualenv** section:
```
/home/YOUR_USERNAME/.virtualenvs/travel-env
```

#### 7. Configure Static Files

In **Web** tab → **Static files** section:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/YOUR_USERNAME/Travel-Booking-System-Django/staticfiles` |
| `/media/` | `/home/YOUR_USERNAME/Travel-Booking-System-Django/media` |

#### 8. Run Migrations

In Bash console:
```bash
cd Travel-Booking-System-Django
workon travel-env
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

#### 9. Reload Web App

Click **Reload** button in Web tab

#### 10. Access Your Site
```
https://YOUR_USERNAME.pythonanywhere.com
```

---

## 🌐 Option 2: Render (Modern & Easy)

**Pros:** Modern platform, Auto-deploys from GitHub, Free SSL  
**Cons:** Free tier has limitations (spins down after inactivity)  
**Free Tier:** 750 hours/month

### Step-by-Step Guide:

#### 1. Create `render.yaml`

```yaml
services:
  - type: web
    name: travel-booking
    env: python
    region: oregon
    buildCommand: "./build.sh"
    startCommand: "gunicorn travel_booking.wsgi:application"
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.0
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: 0
```

#### 2. Create `build.sh`

```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

Make it executable:
```bash
chmod +x build.sh
```

#### 3. Update `requirements.txt`

Add these:
```
gunicorn==21.2.0
whitenoise==6.6.0
psycopg2-binary==2.9.9
dj-database-url==2.1.0
```

#### 4. Update `settings.py`

Add at the top:
```python
import dj_database_url

# Database
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}

# Whitenoise for static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

#### 5. Deploy on Render

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click **New** → **Web Service**
4. Connect your repository
5. Render auto-detects settings from `render.yaml`
6. Click **Create Web Service**

#### 6. Add Environment Variables

In Render Dashboard → Environment:
```
SECRET_KEY=your-secret-key
DEBUG=0
ALLOWED_HOSTS=your-app.onrender.com
```

#### 7. Create Database (Optional)

For PostgreSQL:
1. Create new **PostgreSQL** service
2. Copy **Internal Database URL**
3. Add to environment variables as `DATABASE_URL`

---

## 🚂 Option 3: Railway (Simple & Fast)

**Pros:** Very simple, Auto-deploy from GitHub  
**Cons:** Free trial limited to $5 credit  
**Free Tier:** $5 credit (runs ~500 hours)

### Step-by-Step Guide:

#### 1. Add `Procfile`

```
web: gunicorn travel_booking.wsgi --log-file -
```

#### 2. Update `requirements.txt`

```
gunicorn==21.2.0
dj-database-url==2.1.0
whitenoise==6.6.0
```

#### 3. Update `settings.py`

```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
```

#### 4. Deploy on Railway

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click **New Project** → **Deploy from GitHub repo**
4. Select your repository
5. Add environment variables:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=0
   ```
6. Click **Deploy**

#### 5. Add Database

1. Click **New** → **Database** → **PostgreSQL**
2. Railway automatically sets `DATABASE_URL`

---

## ☁️ Option 4: Heroku (Popular but Paid)

**Note:** Heroku ended free tier in 2022. Now requires payment.

### Quick Setup (If you have paid account):

#### 1. Install Heroku CLI

Download from [heroku.com/cli](https://devcenter.heroku.com/articles/heroku-cli)

#### 2. Create `Procfile`

```
web: gunicorn travel_booking.wsgi
release: python manage.py migrate
```

#### 3. Deploy

```bash
heroku login
heroku create your-app-name
git push heroku main
heroku run python manage.py createsuperuser
heroku open
```

---

## ✅ Post-Deployment Steps

### 1. Create Superuser

```bash
python manage.py createsuperuser
```

### 2. Test Email Configuration

Update email settings for production in `settings.py`:

```python
# Gmail Example
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_APP_PASSWORD')
```

**Gmail Setup:**
1. Enable 2-factor authentication
2. Generate App Password: [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Add to environment variables

### 3. Configure Custom Domain (Optional)

#### On PythonAnywhere:
- Upgrade to paid plan
- Go to Web tab → Set custom domain

#### On Render/Railway:
- Go to Settings → Custom Domains
- Add your domain
- Update DNS records (CNAME)

### 4. Set Up Monitoring

#### Free Monitoring Tools:
- **UptimeRobot**: Monitor uptime (free 50 monitors)
- **Sentry**: Error tracking (free tier available)
- **Google Analytics**: User tracking

### 5. Database Backups

#### Automatic Backups:
```bash
# Create backup script
python manage.py dumpdata > backup_$(date +%Y%m%d).json
```

Set up cron job or scheduler to run daily.

### 6. Security Checklist

- [x] `DEBUG = False`
- [x] Strong `SECRET_KEY`
- [x] HTTPS enabled
- [x] Proper `ALLOWED_HOSTS`
- [x] Security headers configured
- [x] Database credentials secured
- [x] Environment variables set
- [x] `.gitignore` properly configured

---

## 🔧 Common Issues & Solutions

### Issue 1: Static Files Not Loading

**Solution:**
```bash
python manage.py collectstatic --noinput
```

Add to `settings.py`:
```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

### Issue 2: Database Connection Error

**Solution:**
Check `DATABASE_URL` environment variable is set correctly.

### Issue 3: 500 Internal Server Error

**Solution:**
1. Check logs
2. Ensure `DEBUG=False`
3. Set `ALLOWED_HOSTS` correctly
4. Run migrations: `python manage.py migrate`

### Issue 4: Admin Static Files Missing

**Solution:**
```python
# In settings.py
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Run
python manage.py collectstatic
```

---

## 📊 Recommended: PythonAnywhere for Your Project

**Why PythonAnywhere?**
- ✅ Free forever tier
- ✅ No credit card required
- ✅ Easy for Django projects
- ✅ Good documentation
- ✅ Suitable for portfolio/learning projects

**Perfect for:**
- Personal projects
- Portfolio showcases
- Learning deployments
- Small applications

---

## 🎓 Learning Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [PythonAnywhere Django Tutorial](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/)
- [Render Django Guide](https://render.com/docs/deploy-django)
- [Railway Django Guide](https://docs.railway.app/guides/django)

---

## 📞 Need Help?

If you encounter issues:
1. Check platform-specific documentation
2. Review logs for error messages
3. Search Stack Overflow
4. Check Django deployment docs

---

**Good luck with your deployment! 🚀**

Choose PythonAnywhere if you want the easiest free option to get started!
