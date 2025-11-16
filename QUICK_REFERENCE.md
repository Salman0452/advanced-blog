# Quick Reference Guide - Authentication & Authorization

## 🔑 URLs
```python
# Authentication URLs
/accounts/register/  # User registration
/accounts/login/     # User login
/accounts/logout/    # User logout

# Homepage
/                    # Blog home

# Admin
/admin/              # Django admin panel
```

## 👥 User Roles

### Admin
- Full system access
- Manage all posts and comments
- Access admin panel
- User management

### Author  
- Create posts
- Edit/delete own posts
- Add comments

### Reader
- Read posts
- Add/edit own comments

## 🛡️ Permission Mixins

### Import
```python
from accounts.permissions import (
    AdminRequiredMixin,
    AuthorRequiredMixin,
    AuthorOwnerRequiredMixin,
    ReaderRequiredMixin,
    CommentOwnerRequiredMixin,
)
```

### Quick Usage
```python
# Admin only
class MyView(AdminRequiredMixin, CreateView):
    pass

# Authors and Admins
class MyView(AuthorRequiredMixin, CreateView):
    pass

# Post owner or Admin
class MyView(AuthorOwnerRequiredMixin, UpdateView):
    pass

# All authenticated users
class MyView(ReaderRequiredMixin, CreateView):
    pass

# Comment owner or Admin
class MyView(CommentOwnerRequiredMixin, UpdateView):
    pass
```

## 📝 Forms

### Registration Form
```python
from accounts.forms import UserRegistrationForm

# Fields: username, email, first_name, last_name, role, password1, password2
# Bootstrap 5 styled
# Auto-saves with role
```

### Login Form
```python
from accounts.forms import UserLoginForm

# Fields: username, password, remember_me
# Bootstrap 5 styled
# Handles session expiry
```

## 🎨 Template Usage

### Base Template
```django
{% extends 'base.html' %}

{% block title %}Page Title{% endblock %}

{% block content %}
    <!-- Your content here -->
{% endblock %}
```

### Check User Role
```django
{% if user.is_authenticated %}
    {% if user.is_admin %}
        <!-- Admin content -->
    {% elif user.is_author %}
        <!-- Author content -->
    {% elif user.is_reader %}
        <!-- Reader content -->
    {% endif %}
{% endif %}
```

### Display User Info
```django
{{ user.username }}
{{ user.email }}
{{ user.role }}
{{ user.get_full_name }}
```

### Show Role Badge
```django
<span class="user-badge badge-{{ user.role|lower }}">
    {{ user.role }}
</span>
```

## 💬 Messages

### Add Message in View
```python
from django.contrib import messages

# Success
messages.success(request, 'Operation successful!')

# Error
messages.error(request, 'Something went wrong.')

# Warning
messages.warning(request, 'Be careful!')

# Info
messages.info(request, 'Here is some info.')
```

### Display in Template (already in base.html)
```django
{% if messages %}
    {% for message in messages %}
        <div class="alert alert-{{ message.tags }}">
            {{ message }}
        </div>
    {% endfor %}
{% endif %}
```

## 🔐 Authentication Checks

### In View (Python)
```python
# Check if authenticated
if request.user.is_authenticated:
    pass

# Check role
if request.user.is_admin():
    pass

if request.user.is_author():
    pass

if request.user.is_reader():
    pass

# Get user info
username = request.user.username
email = request.user.email
role = request.user.role
```

### In Template (Django)
```django
{% if user.is_authenticated %}
    <!-- Authenticated content -->
{% else %}
    <!-- Guest content -->
{% endif %}

{% if user.is_admin %}
    <!-- Admin content -->
{% endif %}
```

## 📊 Model Relationships

### User → Posts (1:N)
```python
# Get all posts by user
user.posts.all()

# Get post author
post.author
```

### User → Comments (1:N)
```python
# Get all comments by user
user.comments.all()

# Get comment author
comment.author
```

## 🚀 Common Patterns

### Create View with Auto Author
```python
class PostCreateView(AuthorRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
```

### Filter by Current User
```python
class MyPostsView(AuthorRequiredMixin, ListView):
    model = Post
    
    def get_queryset(self):
        if self.request.user.is_admin():
            return Post.objects.all()
        return Post.objects.filter(author=self.request.user)
```

### Custom Permission Check
```python
def has_permission(self):
    if not self.request.user.is_authenticated:
        return False
    
    # Custom logic
    obj = self.get_object()
    return obj.author == self.request.user or self.request.user.is_admin()
```

## ⚙️ Settings (already configured)

```python
# Custom user model
AUTH_USER_MODEL = 'accounts.User'

# Redirect URLs
LOGIN_REDIRECT_URL = 'blog:home'
LOGOUT_REDIRECT_URL = 'blog:home'
LOGIN_URL = 'accounts:login'
```

## 🧪 Testing Checklist

- [ ] Register user with each role (Admin, Author, Reader)
- [ ] Login with valid credentials
- [ ] Login with invalid credentials (should fail)
- [ ] Logout functionality
- [ ] "Remember Me" checkbox (session persistence)
- [ ] Access protected view without login (should redirect)
- [ ] Access admin view as non-admin (should deny)
- [ ] Author can edit own post
- [ ] Author cannot edit others' posts
- [ ] Reader cannot create posts
- [ ] Admin can edit all posts
- [ ] User sees correct permissions in UI
- [ ] Role badges display correctly

## 📱 Bootstrap Classes Used

```css
/* Forms */
.form-control       /* Input styling */
.form-label         /* Label styling */
.form-check-input   /* Checkbox styling */

/* Buttons */
.btn-primary        /* Primary actions */
.btn-danger         /* Destructive actions */
.btn-outline-*      /* Outlined buttons */

/* Layout */
.container          /* Main container */
.row                /* Row layout */
.col-md-*           /* Responsive columns */

/* Components */
.card               /* Card component */
.navbar             /* Navigation bar */
.alert              /* Alert messages */
.badge              /* Role badges */

/* Custom */
.user-badge         /* Role badge styling */
.badge-admin        /* Admin badge (red) */
.badge-author       /* Author badge (blue) */
.badge-reader       /* Reader badge (gray) */
```

## 🐛 Common Issues & Solutions

### Issue: Permission denied for authenticated user
**Solution**: Check if user has correct role and mixin matches requirement

### Issue: Login redirect not working
**Solution**: Check `LOGIN_REDIRECT_URL` in settings and `next` parameter in URL

### Issue: Template not found
**Solution**: Verify `DIRS` in TEMPLATES setting includes templates folder

### Issue: Static files not loading
**Solution**: Run `python manage.py collectstatic` and check STATIC_URL

### Issue: Form validation errors not showing
**Solution**: Check template includes `{{ form.field.errors }}`

## 📚 File Locations

```
accounts/
├── forms.py          # UserRegistrationForm, UserLoginForm
├── views.py          # RegisterView, LoginView, LogoutView
├── permissions.py    # All permission mixins
├── models.py         # User model
└── urls.py           # Authentication URLs

templates/
├── base.html         # Base template
├── accounts/         # Authentication templates
└── blog/             # Blog templates

static/
└── css/              # Custom CSS
```

## 💡 Pro Tips

1. **Always import permission mixins before generic views** in class declaration
2. **Use `form_valid()` to set author automatically** in create views
3. **Check `is_admin()` first** in permission logic for admin override
4. **Use `select_related()` in querysets** for better performance
5. **Add success messages** for better UX
6. **Use `get_queryset()` to filter** data by user role
7. **Combine mixins** for complex permissions
8. **Test with different user roles** before deployment

---

**Need help?** Check `AUTHENTICATION_README.md` for detailed documentation!
