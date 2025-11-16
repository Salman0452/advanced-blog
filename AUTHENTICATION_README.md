# Advanced Blog - Authentication & Authorization

## Overview
A Django blog application with comprehensive authentication and role-based authorization system.

## Features Implemented

### 1. Authentication System
- **User Registration** - New users can create accounts with username, email, and password
- **User Login** - Secure login with "Remember Me" functionality
- **User Logout** - Safe logout with confirmation page
- **Session Management** - Configurable session expiry based on "Remember Me" option

### 2. Role-Based Authorization
Three distinct user roles with specific permissions:

#### Admin Role
- Full access to all features
- Manage all posts (create, edit, delete)
- Moderate comments
- Access to Django admin panel
- User management capabilities

#### Author Role
- Create new blog posts
- Edit and delete own posts
- Add comments to any post
- View all published content

#### Reader Role
- Read all published posts
- Add comments to posts
- Edit own comments
- Basic authenticated user features

### 3. Custom Permission Mixins
Located in `accounts/permissions.py`:

- **`RoleRequiredMixin`** - Base mixin for role-based access control
- **`AdminRequiredMixin`** - Requires Admin role
- **`AuthorRequiredMixin`** - Requires Author or Admin role
- **`AuthorOwnerRequiredMixin`** - Requires user to be post owner or Admin
- **`ReaderRequiredMixin`** - Requires any authenticated user
- **`CommentOwnerRequiredMixin`** - Requires user to be comment owner or Admin

### 4. Templates
All templates use **Bootstrap 5** for modern, responsive design:

- **`base.html`** - Main template with navigation, messages, and footer
- **`accounts/register.html`** - User registration form
- **`accounts/login.html`** - User login form
- **`accounts/logout_confirm.html`** - Logout confirmation page
- **`blog/home.html`** - Homepage with role information

## File Structure

```
A3/
├── accounts/
│   ├── forms.py              # Registration & Login forms
│   ├── views.py              # Authentication views
│   ├── permissions.py        # Custom permission mixins
│   ├── models.py             # Custom User model with roles
│   ├── admin.py              # User admin configuration
│   └── urls.py               # Authentication URLs
├── blog/
│   ├── models.py             # Post, Comment, Category, Tag models
│   ├── admin.py              # Blog admin configuration
│   └── urls.py               # Blog URLs
├── templates/
│   ├── base.html             # Base template
│   ├── accounts/             # Authentication templates
│   └── blog/                 # Blog templates
├── static/
│   └── css/                  # Custom CSS
└── advanced_blog/
    ├── settings.py           # Project settings
    └── urls.py               # Main URL configuration

```

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Apply Migrations
```bash
python manage.py migrate
```

### 3. Create Superuser
```bash
python manage.py createsuperuser
```

### 4. Run Development Server
```bash
python manage.py runserver
```

### 5. Access the Application
- **Homepage:** http://127.0.0.1:8000/
- **Register:** http://127.0.0.1:8000/accounts/register/
- **Login:** http://127.0.0.1:8000/accounts/login/
- **Admin Panel:** http://127.0.0.1:8000/admin/

## Using Permission Mixins

### Example: Protect a View for Authors Only
```python
from django.views.generic import CreateView
from accounts.permissions import AuthorRequiredMixin
from blog.models import Post

class PostCreateView(AuthorRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'category']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
```

### Example: Ensure User Owns the Post
```python
from django.views.generic import UpdateView
from accounts.permissions import AuthorOwnerRequiredMixin
from blog.models import Post

class PostUpdateView(AuthorOwnerRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'category', 'status']
```

### Example: Admin Only Access
```python
from django.views.generic import DeleteView
from accounts.permissions import AdminRequiredMixin
from blog.models import Post

class PostDeleteView(AdminRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:home')
```

## User Model

The custom User model extends Django's `AbstractUser` with:
- **`role`** - CharField with choices: Admin, Author, Reader
- **`bio`** - TextField for user biography
- **`profile_picture`** - ImageField for profile photos

Helper methods:
- `is_admin()` - Returns True if user is Admin
- `is_author()` - Returns True if user is Author
- `is_reader()` - Returns True if user is Reader

## Authentication Forms

### UserRegistrationForm
- Username, email, first name, last name
- Role selection (Admin, Author, Reader)
- Password with confirmation
- Bootstrap 5 styling

### UserLoginForm
- Username and password
- "Remember Me" checkbox
- Bootstrap 5 styling

## Key Settings

In `advanced_blog/settings.py`:
```python
# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Authentication URLs
LOGIN_REDIRECT_URL = 'blog:home'
LOGOUT_REDIRECT_URL = 'blog:home'
LOGIN_URL = 'accounts:login'
```

## Bootstrap 5 Integration

All templates use Bootstrap 5 loaded via CDN:
- Responsive navbar with dropdown menus
- Form styling with validation feedback
- Alert messages for user feedback
- Card components for content display
- Custom color scheme and badge styles

## Security Features

- CSRF protection on all forms
- Password validation (length, similarity, common passwords)
- Session management with configurable expiry
- Permission checks on all protected views
- Redirect authenticated users from login/register pages

## Next Steps

To extend this authentication system:

1. **Add Password Reset** - Implement forgot password functionality
2. **Email Verification** - Verify user emails on registration
3. **Profile Management** - Allow users to update their profiles
4. **Social Authentication** - Add OAuth login options
5. **Two-Factor Authentication** - Add extra security layer

## Testing

To test the role-based permissions:

1. Create users with different roles via registration page
2. Login as each user type
3. Observe different permissions in the navigation menu
4. Try accessing protected views with different roles

## Support

For issues or questions about the authentication system, please refer to the Django documentation:
- [Django Authentication](https://docs.djangoproject.com/en/5.2/topics/auth/)
- [Django Permissions](https://docs.djangoproject.com/en/5.2/topics/auth/default/#permissions-and-authorization)
