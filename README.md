# Advanced Django Blog Platform

A full-featured, production-ready blog platform built with Django 5.2.8, featuring user authentication, role-based permissions, rich text editing, comment system, and comprehensive admin interface.

## 🌟 Features

### User Management
- **Custom User Model** with role-based permissions (Admin, Author, Reader)
- User registration and authentication
- Profile management with bio and profile pictures
- Role-based access control

### Blog Functionality
- **Rich Text Editor** (CKEditor) for post content
- Post categories and tags for organization
- Post status management (Draft, Published, Archived)
- Featured images for posts
- View counter for posts
- Search functionality
- Post slugs for SEO-friendly URLs

### Comment System
- Threaded comments (nested replies)
- Comment moderation (approval system)
- Comment notifications to post authors
- Reply notifications to parent comment authors

### Admin Interface
- **Customized Django Admin** with advanced features:
  - List displays with post/comment counts
  - Advanced filters (status, category, tags, dates)
  - Bulk actions (publish, approve, archive, etc.)
  - Search functionality across all models
  - Date hierarchies for easy navigation
  - Optimized queries with select_related and prefetch_related

### Notifications System
- **Email notifications** for:
  - Post publication (to admins)
  - New comments (to post authors)
  - Comment replies (to parent comment authors)
- Django signals for automated notifications

### Media Handling
- Configured MEDIA_URL and MEDIA_ROOT
- Image uploads for posts and profiles
- WhiteNoise for efficient static file serving

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd A3
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your configuration
   # At minimum, set SECRET_KEY for production
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files** (for production)
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Populate sample data** (optional)
   ```bash
   python manage.py populate_blog
   ```

9. **Run development server**
   ```bash
   python manage.py runserver
   ```

10. **Access the application**
    - Main site: http://127.0.0.1:8000/
    - Admin panel: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
A3/
├── accounts/                 # User authentication and profiles
│   ├── models.py            # Custom User model
│   ├── views.py             # Authentication views
│   ├── forms.py             # User forms
│   └── admin.py             # User admin customization
├── blog/                    # Main blog application
│   ├── models.py            # Post, Category, Tag, Comment models
│   ├── views.py             # Blog views
│   ├── forms.py             # Blog forms
│   ├── signals.py           # Notification signals
│   ├── admin.py             # Blog admin customization
│   └── management/
│       └── commands/
│           └── populate_blog.py  # Sample data generator
├── advanced_blog/           # Project settings
│   ├── settings.py          # Main settings (with deployment config)
│   ├── urls.py              # URL configuration
│   └── wsgi.py              # WSGI configuration
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── accounts/            # Authentication templates
│   └── blog/                # Blog templates
├── static/                  # Static files (CSS, JS)
├── media/                   # User uploaded files
├── staticfiles/             # Collected static files (production)
├── requirements.txt         # Python dependencies
├── Procfile                 # Heroku deployment config
├── runtime.txt              # Python version for Heroku
└── manage.py                # Django management script
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database (Production)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

### Database Configuration

**Development (SQLite)**
- Default configuration uses SQLite
- No additional setup required

**Production (PostgreSQL)**
- Set `DATABASE_URL` environment variable
- Format: `postgresql://user:password@host:port/database`

### Email Configuration

**Development**
- Uses console backend (emails printed to terminal)
- No configuration needed

**Production**
- Configure SMTP settings in `.env`
- Recommended: Use Gmail with App Password or SendGrid

## 🚢 Deployment

### Heroku Deployment

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

4. **Add PostgreSQL addon**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

5. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY='your-secret-key'
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS='your-app-name.herokuapp.com'
   ```

6. **Deploy**
   ```bash
   git push heroku main
   ```

7. **Run migrations**
   ```bash
   heroku run python manage.py migrate
   ```

8. **Create superuser**
   ```bash
   heroku run python manage.py createsuperuser
   ```

### PythonAnywhere Deployment

1. **Upload your code**
   - Use Git or PythonAnywhere file upload

2. **Create virtual environment**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.11 myenv
   pip install -r requirements.txt
   ```

3. **Configure web app**
   - WSGI configuration file: `/var/www/yourusername_pythonanywhere_com_wsgi.py`
   - Add your project path to sys.path
   - Set environment variables in WSGI file

4. **Set up static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

5. **Configure static files mapping**
   - URL: `/static/`
   - Directory: `/path/to/project/staticfiles/`
   - URL: `/media/`
   - Directory: `/path/to/project/media/`

6. **Run migrations**
   ```bash
   python manage.py migrate
   ```

### Using WhiteNoise (Included)

WhiteNoise is already configured for serving static files efficiently:
- Automatic compression
- Cache-friendly file names
- No additional web server configuration needed

## 📊 Admin Features

### Post Management
- **List View**: Shows title, author, category, status, comments, views, dates
- **Filters**: Status, category, tags, dates, author
- **Actions**: Bulk publish, draft, archive posts
- **Search**: Search by title, content, author

### Comment Moderation
- **List View**: Shows preview, author, post, approval status
- **Filters**: Approval status, date, post
- **Actions**: Bulk approve/unapprove, delete
- **Quick Edit**: Edit approval status directly in list

### User Management
- **List View**: Shows username, email, role, posts count, status
- **Filters**: Role, staff status, active status, join date
- **Actions**: Bulk activate/deactivate, change roles
- **Extended Fields**: Bio, profile picture, role

### Category & Tag Management
- **Post Counts**: See number of posts per category/tag
- **Auto-slugification**: Automatic URL-friendly slugs
- **Search**: Find categories/tags quickly

## 🔔 Notifications

The blog automatically sends email notifications for:

1. **Post Publication**
   - Sent to all Admin users
   - Includes post details and link

2. **New Comments**
   - Sent to post author
   - Not sent if author comments on own post

3. **Comment Replies**
   - Sent to parent comment author
   - Maintains conversation thread awareness

### Configuring Notifications

**Development**: Emails are printed to console

**Production**: Configure SMTP settings in `.env`

Example Gmail configuration:
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=yourname@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

**Note**: For Gmail, you need to create an [App Password](https://support.google.com/accounts/answer/185833)

## 🔐 Security Features

### Production Security Settings
When `DEBUG=False`, the following security features are automatically enabled:

- **HTTPS Redirect**: All HTTP requests redirected to HTTPS
- **Secure Cookies**: Session and CSRF cookies only sent over HTTPS
- **XSS Protection**: Browser XSS filter enabled
- **Content Type Sniffing**: Prevented
- **Clickjacking Protection**: X-Frame-Options set to DENY
- **HSTS**: HTTP Strict Transport Security with 1-year duration

### Best Practices
1. **Never commit** `.env` file or `SECRET_KEY`
2. **Use strong passwords** for admin accounts
3. **Keep dependencies updated**: `pip install -U -r requirements.txt`
4. **Regular backups** of database and media files
5. **Monitor logs** for suspicious activity

## 📝 Common Tasks

### Create a new post
```python
from blog.models import Post, Category
from accounts.models import User

author = User.objects.get(username='admin')
category = Category.objects.get(name='Technology')

post = Post.objects.create(
    title='My First Post',
    content='<p>This is the post content</p>',
    author=author,
    category=category,
    status='published'
)
```

### Moderate comments
```bash
# In admin interface: /admin/blog/comment/
# Or via shell:
from blog.models import Comment

# Approve all pending comments
Comment.objects.filter(is_approved=False).update(is_approved=True)
```

### Generate sample data
```bash
python manage.py populate_blog
```

## 🧪 Testing

Run tests with:
```bash
python manage.py test
```

## 📚 Documentation

- [Django Documentation](https://docs.djangoproject.com/)
- [CKEditor Documentation](https://django-ckeditor.readthedocs.io/)
- [WhiteNoise Documentation](http://whitenoise.evans.io/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- Django Software Foundation
- CKEditor team
- WhiteNoise contributors
- All open-source contributors

## 📞 Support

For issues, questions, or contributions, please open an issue on GitHub.

## 🗺️ Roadmap

- [ ] Add REST API support
- [ ] Implement social media sharing
- [ ] Add post analytics dashboard
- [ ] Implement SEO metadata
- [ ] Add post scheduling
- [ ] Multi-language support
- [ ] Integration with social auth (Google, GitHub, etc.)
- [ ] Advanced search with filters
- [ ] Post bookmarking/favorites
- [ ] Newsletter subscription system

---

**Built with ❤️ using Django**
