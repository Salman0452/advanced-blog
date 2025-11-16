# Deployment Guide for Advanced Django Blog

This guide provides detailed instructions for deploying your Django blog to production environments.

## Pre-Deployment Checklist

- [ ] All features tested locally
- [ ] Environment variables configured
- [ ] Static files collected
- [ ] Media files backed up
- [ ] Database backed up
- [ ] SECRET_KEY changed from default
- [ ] DEBUG set to False
- [ ] ALLOWED_HOSTS configured
- [ ] Dependencies updated in requirements.txt

## Option 1: Heroku Deployment

### Prerequisites
- Heroku account (free tier available)
- Heroku CLI installed
- Git repository initialized

### Step-by-Step Deployment

#### 1. Prepare Your Application

Ensure all deployment files are in place:
- `Procfile` - Tells Heroku how to run your app
- `runtime.txt` - Specifies Python version
- `requirements.txt` - Lists all dependencies

#### 2. Install Heroku CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Ubuntu/Debian
curl https://cli-assets.heroku.com/install.sh | sh

# Windows
# Download installer from https://devcenter.heroku.com/articles/heroku-cli
```

#### 3. Login to Heroku

```bash
heroku login
```

#### 4. Create Heroku Application

```bash
# Create new app
heroku create your-blog-name

# Or create with specific region
heroku create your-blog-name --region eu
```

#### 5. Add PostgreSQL Database

```bash
# Add free PostgreSQL addon
heroku addons:create heroku-postgresql:mini

# Verify database was added
heroku config:get DATABASE_URL
```

#### 6. Configure Environment Variables

```bash
# Generate a new SECRET_KEY
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Set environment variables
heroku config:set SECRET_KEY='your-generated-secret-key'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS='your-blog-name.herokuapp.com'

# Email configuration (optional)
heroku config:set EMAIL_HOST='smtp.gmail.com'
heroku config:set EMAIL_PORT=587
heroku config:set EMAIL_USE_TLS=True
heroku config:set EMAIL_HOST_USER='your-email@gmail.com'
heroku config:set EMAIL_HOST_PASSWORD='your-app-password'
heroku config:set DEFAULT_FROM_EMAIL='noreply@yourblog.com'
```

#### 7. Deploy to Heroku

```bash
# Add Heroku remote (if not automatically added)
heroku git:remote -a your-blog-name

# Deploy
git push heroku main
```

#### 8. Run Migrations

```bash
heroku run python manage.py migrate
```

#### 9. Collect Static Files

```bash
heroku run python manage.py collectstatic --noinput
```

#### 10. Create Superuser

```bash
heroku run python manage.py createsuperuser
```

#### 11. Optional: Populate Sample Data

```bash
heroku run python manage.py populate_blog
```

#### 12. Open Your Application

```bash
heroku open
```

### Managing Your Heroku App

```bash
# View logs
heroku logs --tail

# Access Django shell
heroku run python manage.py shell

# Scale dynos
heroku ps:scale web=1

# Restart application
heroku restart

# View app info
heroku info
```

### Updating Your Heroku App

```bash
# Make changes to your code
git add .
git commit -m "Description of changes"
git push heroku main

# Migrations will run automatically (defined in Procfile)
```

## Option 2: PythonAnywhere Deployment

### Prerequisites
- PythonAnywhere account (free tier available)
- Project code uploaded or accessible via Git

### Step-by-Step Deployment

#### 1. Upload Your Code

**Option A: Using Git**
```bash
# In PythonAnywhere Bash console
git clone https://github.com/yourusername/your-blog-repo.git
cd your-blog-repo
```

**Option B: File Upload**
- Use PythonAnywhere's file upload interface
- Upload as a zip file and extract

#### 2. Create Virtual Environment

```bash
# In PythonAnywhere Bash console
cd your-blog-repo
mkvirtualenv --python=/usr/bin/python3.11 myblog_env
pip install -r requirements.txt
```

#### 3. Configure Web App

1. Go to Web tab in PythonAnywhere dashboard
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select Python 3.11

#### 4. Configure WSGI File

Edit the WSGI configuration file (path shown in Web tab):

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/yourusername/your-blog-repo'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['SECRET_KEY'] = 'your-secret-key-here'
os.environ['DEBUG'] = 'False'
os.environ['ALLOWED_HOSTS'] = 'yourusername.pythonanywhere.com'
os.environ['DATABASE_URL'] = 'sqlite:////home/yourusername/your-blog-repo/db.sqlite3'

# Django WSGI application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_blog.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

#### 5. Configure Virtual Environment

In the Web tab, set the virtualenv path:
```
/home/yourusername/.virtualenvs/myblog_env
```

#### 6. Configure Static Files

In the Web tab, add static file mappings:

| URL | Directory |
|-----|-----------|
| /static/ | /home/yourusername/your-blog-repo/staticfiles |
| /media/ | /home/yourusername/your-blog-repo/media |

#### 7. Collect Static Files

```bash
# In PythonAnywhere Bash console
cd your-blog-repo
workon myblog_env
python manage.py collectstatic --noinput
```

#### 8. Run Migrations

```bash
python manage.py migrate
```

#### 9. Create Superuser

```bash
python manage.py createsuperuser
```

#### 10. Reload Web App

Click the "Reload" button in the Web tab.

### Using PostgreSQL on PythonAnywhere (Paid Accounts)

1. Create PostgreSQL database in Databases tab
2. Note the connection details
3. Update DATABASE_URL in WSGI file:
```python
os.environ['DATABASE_URL'] = 'postgresql://username:password@host/database'
```

## Option 3: VPS Deployment (DigitalOcean, Linode, etc.)

### Prerequisites
- VPS with Ubuntu 22.04 or similar
- SSH access to your server
- Domain name (optional)

### Quick Setup

#### 1. Update System

```bash
sudo apt update && sudo apt upgrade -y
```

#### 2. Install Dependencies

```bash
sudo apt install python3.11 python3.11-venv python3-pip nginx postgresql postgresql-contrib -y
```

#### 3. Create PostgreSQL Database

```bash
sudo -u postgres psql

# In PostgreSQL shell:
CREATE DATABASE blogdb;
CREATE USER bloguser WITH PASSWORD 'strong_password_here';
ALTER ROLE bloguser SET client_encoding TO 'utf8';
ALTER ROLE bloguser SET default_transaction_isolation TO 'read committed';
ALTER ROLE bloguser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE blogdb TO bloguser;
\q
```

#### 4. Set Up Application

```bash
# Create app directory
sudo mkdir -p /var/www/blog
sudo chown $USER:$USER /var/www/blog
cd /var/www/blog

# Clone repository
git clone https://github.com/yourusername/your-blog-repo.git .

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 5. Configure Environment

```bash
# Create .env file
nano .env
```

Add:
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgresql://bloguser:strong_password_here@localhost:5432/blogdb
```

#### 6. Prepare Django Application

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

#### 7. Configure Gunicorn

Create systemd service file:
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Add:
```ini
[Unit]
Description=gunicorn daemon for Django blog
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/blog
EnvironmentFile=/var/www/blog/.env
ExecStart=/var/www/blog/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/var/www/blog/gunicorn.sock \
          advanced_blog.wsgi:application

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

#### 8. Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/blog
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/blog/staticfiles/;
    }
    
    location /media/ {
        alias /var/www/blog/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/blog/gunicorn.sock;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 9. Set Up SSL (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

## Post-Deployment

### 1. Test Your Application

- Visit your site
- Test user registration
- Create a test post
- Add comments
- Test admin interface

### 2. Monitor Logs

**Heroku:**
```bash
heroku logs --tail
```

**PythonAnywhere:**
- Check error log in Web tab
- Check server log in Web tab

**VPS:**
```bash
sudo journalctl -u gunicorn -f
sudo tail -f /var/log/nginx/error.log
```

### 3. Set Up Backups

**Database Backups:**
```bash
# PostgreSQL
pg_dump dbname > backup.sql

# Heroku
heroku pg:backups:capture
heroku pg:backups:download
```

**Media Files:**
```bash
tar -czf media-backup.tar.gz media/
```

### 4. Performance Optimization

- Enable caching
- Use CDN for static files
- Optimize database queries
- Monitor with tools like New Relic or Sentry

## Troubleshooting

### Common Issues

**Static files not loading:**
```bash
python manage.py collectstatic --noinput
```

**Database connection errors:**
- Verify DATABASE_URL is correct
- Check database credentials
- Ensure database server is running

**500 Server Error:**
- Check DEBUG=False is set
- Review error logs
- Verify all environment variables are set

**Email not sending:**
- Check email configuration in .env
- Verify SMTP credentials
- Check firewall settings for email ports

## Security Reminders

1. ✅ Use strong SECRET_KEY
2. ✅ Set DEBUG=False in production
3. ✅ Use HTTPS (SSL certificate)
4. ✅ Keep dependencies updated
5. ✅ Regular database backups
6. ✅ Monitor logs for suspicious activity
7. ✅ Use environment variables for sensitive data
8. ✅ Implement rate limiting
9. ✅ Regular security audits

## Maintenance

### Regular Updates

```bash
# Update dependencies
pip install -U -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart application
# Heroku: automatic
# PythonAnywhere: Reload button
# VPS: sudo systemctl restart gunicorn
```

### Database Maintenance

```bash
# Django shell
python manage.py shell

# Database shell
python manage.py dbshell

# Clear sessions
python manage.py clearsessions
```

## Support

For deployment issues:
- Check Django deployment checklist: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
- Heroku support: https://devcenter.heroku.com/
- PythonAnywhere forums: https://www.pythonanywhere.com/forums/

---

**Happy Deploying! 🚀**
