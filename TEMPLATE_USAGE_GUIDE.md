# Template Usage Quick Reference

## Template Components & Usage

### 1. Base Template Features

#### Flash Messages
All templates automatically display Django messages:
```python
from django.contrib import messages

# In your view
messages.success(request, 'Post published successfully!')
messages.error(request, 'Unable to save post.')
messages.warning(request, 'Post is still in draft mode.')
messages.info(request, 'Post has been updated.')
```

#### User Role Badges
Automatically displayed based on user role:
- **Admin**: Red badge
- **Author**: Blue badge  
- **Reader**: Gray badge

### 2. Image Handling in Templates

#### Featured Images (Post List/Detail)
```django
{% if post.featured_image %}
    <img src="{{ post.featured_image.url }}" class="post-image" alt="{{ post.title }}">
{% else %}
    <div class="bg-light d-flex align-items-center justify-content-center" style="height: 300px;">
        <i class="bi bi-image text-muted" style="font-size: 4rem;"></i>
    </div>
{% endif %}
```

#### CKEditor Images in Content
Images uploaded via CKEditor are automatically embedded in the content:
```django
<div class="post-content">
    {{ post.content|safe }}
</div>
```

### 3. Navigation Menu

The navigation automatically shows/hides items based on:
- Authentication status
- User role (Admin, Author, Reader)

**For Authors/Admins:**
- My Posts
- My Drafts
- Create Post
- Moderate Comments (Admin only)

### 4. Common Template Patterns

#### Post Card (Reusable Pattern)
```django
<article class="card mb-4">
    {% if post.featured_image %}
        <img src="{{ post.featured_image.url }}" class="card-img-top post-image" alt="{{ post.title }}">
    {% endif %}
    <div class="card-body">
        <h2 class="card-title">
            <a href="{% url 'blog:post_detail' post.slug %}">{{ post.title }}</a>
        </h2>
        
        <div class="mb-3">
            <small class="text-muted">
                <i class="bi bi-person"></i> {{ post.author.get_full_name|default:post.author.username }}
                <i class="bi bi-calendar"></i> {{ post.published_at|date:"M d, Y" }}
            </small>
        </div>

        {% if post.category %}
            <a href="{% url 'blog:category_detail' post.category.slug %}" class="badge bg-primary">
                {{ post.category.name }}
            </a>
        {% endif %}

        <p class="card-text mt-3">
            {{ post.excerpt|default:post.content|truncatewords:50|striptags }}
        </p>

        <a href="{% url 'blog:post_detail' post.slug %}" class="btn btn-outline-primary">
            Read More <i class="bi bi-arrow-right"></i>
        </a>
    </div>
</article>
```

#### Pagination (Reusable Pattern)
```django
{% if is_paginated %}
    <nav aria-label="Page navigation">
        <ul class="pagination justify-content-center">
            {% if page_obj.has_previous %}
                <li class="page-item">
                    <a class="page-link" href="?page=1">First</a>
                </li>
                <li class="page-item">
                    <a class="page-link" href="?page={{ page_obj.previous_page_number }}">Previous</a>
                </li>
            {% endif %}

            <li class="page-item active">
                <span class="page-link">
                    Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}
                </span>
            </li>

            {% if page_obj.has_next %}
                <li class="page-item">
                    <a class="page-link" href="?page={{ page_obj.next_page_number }}">Next</a>
                </li>
                <li class="page-item">
                    <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}">Last</a>
                </li>
            {% endif %}
        </ul>
    </nav>
{% endif %}
```

### 5. Form Rendering

#### Bootstrap Form Field Pattern
```django
<div class="mb-3">
    <label for="{{ form.field_name.id_for_label }}" class="form-label">
        Field Label {% if field.field.required %}<span class="text-danger">*</span>{% endif %}
    </label>
    {{ form.field_name }}
    {% if form.field_name.errors %}
        <div class="text-danger small mt-1">
            {% for error in form.field_name.errors %}
                <div>{{ error }}</div>
            {% endfor %}
        </div>
    {% endif %}
    {% if form.field_name.help_text %}
        <div class="form-text">{{ form.field_name.help_text }}</div>
    {% endif %}
</div>
```

### 6. Icons Reference

Common Bootstrap Icons used in templates:
- `bi-house-door` - Home
- `bi-folder` / `bi-folder-fill` - Categories
- `bi-tags` / `bi-tags-fill` - Tags
- `bi-search` - Search
- `bi-person-circle` - User
- `bi-pencil-square` - Edit
- `bi-trash` - Delete
- `bi-eye` - Views
- `bi-chat-dots` - Comments
- `bi-calendar3` - Date
- `bi-arrow-right` - Navigation

Full icon list: https://icons.getbootstrap.com/

### 7. CSS Classes Reference

#### Card Styles
- `.card` - Standard card
- `.card.shadow-sm` - Card with subtle shadow
- `.card.h-100` - Full height card (for grid layouts)

#### Button Styles
- `.btn-primary` - Primary action
- `.btn-outline-primary` - Secondary action
- `.btn-danger` - Delete/destructive action
- `.btn-success` - Confirm/positive action
- `.btn-sm` - Small button

#### Badge Styles
- `.badge.bg-primary` - Category badge
- `.badge.bg-secondary` - Tag badge
- `.badge.bg-success` - Status: Published
- `.badge.bg-warning` - Status: Draft
- `.user-badge.badge-admin` - Admin role
- `.user-badge.badge-author` - Author role
- `.user-badge.badge-reader` - Reader role

#### Image Styles
- `.post-image` - List view image (300px height)
- `.post-image-detail` - Detail view image (500px max)
- `.post-thumbnail` - Small thumbnail (250px height)

### 8. Template Context Variables

#### Home Page
- `user` - Current authenticated user
- `posts` - Latest published posts (limit 5)

#### Post List
- `posts` - Paginated post queryset
- `page_obj` - Pagination object
- `is_paginated` - Boolean for pagination display
- `categories` - All categories (sidebar)
- `tags` - Popular tags (sidebar)

#### Post Detail
- `post` - Post object
- `comments` - Approved comments for the post
- `comment_form` - Form for adding comments
- `can_edit` - Boolean for edit permissions

#### Category/Tag Detail
- `category` / `tag` - Category/Tag object
- `posts` - Filtered posts
- `page_obj` - Pagination object

#### Post Form
- `form` - Post creation/edit form
- `form_title` - "Create Post" or "Edit Post"
- `submit_text` - "Create" or "Update"

#### My Posts
- `posts` - User's posts
- `page_obj` - Pagination object

### 9. Custom Template Tags (If Needed)

To create custom template tags, create `blog/templatetags/blog_tags.py`:

```python
from django import template

register = template.Library()

@register.filter
def reading_time(content):
    """Calculate estimated reading time"""
    words = len(content.split())
    minutes = words // 200  # Average reading speed
    return max(1, minutes)

# Usage in template:
# {{ post.content|reading_time }} min read
```

### 10. JavaScript Integration

Add custom JavaScript in templates:

```django
{% block extra_js %}
<script>
    // Confirm delete action
    document.querySelectorAll('.delete-confirm').forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Are you sure?')) {
                e.preventDefault();
            }
        });
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            alert.classList.remove('show');
            setTimeout(() => alert.remove(), 150);
        });
    }, 5000);
</script>
{% endblock %}
```

### 11. Responsive Grid Layouts

```django
<div class="row">
    {% for item in items %}
        <div class="col-12 col-md-6 col-lg-4 mb-4">
            <!-- Card content -->
        </div>
    {% endfor %}
</div>
```

Breakpoints:
- `col-12` - Full width on mobile
- `col-md-6` - 2 columns on tablet
- `col-lg-4` - 3 columns on desktop

### 12. Search Form Pattern

```django
<form method="get" action="{% url 'blog:post_search' %}">
    <div class="input-group">
        <input type="text" name="query" class="form-control" 
               placeholder="Search..." value="{{ request.GET.query }}">
        <button class="btn btn-primary" type="submit">
            <i class="bi bi-search"></i> Search
        </button>
    </div>
</form>
```

### 13. Empty States

```django
{% if posts %}
    <!-- Display posts -->
{% else %}
    <div class="alert alert-info text-center py-5">
        <i class="bi bi-info-circle" style="font-size: 3rem;"></i>
        <p class="mt-3">No posts available yet.</p>
        {% if user.is_author %}
            <a href="{% url 'blog:post_create' %}" class="btn btn-primary">
                Create Your First Post
            </a>
        {% endif %}
    </div>
{% endif %}
```

### 14. Breadcrumbs

```django
<nav aria-label="breadcrumb">
    <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="{% url 'blog:home' %}">Home</a></li>
        <li class="breadcrumb-item"><a href="{% url 'blog:category_list' %}">Categories</a></li>
        <li class="breadcrumb-item active" aria-current="page">{{ category.name }}</li>
    </ol>
</nav>
```

### 15. Permission-Based Display

```django
{% if user.is_authenticated %}
    {% if user.is_author or user.is_admin %}
        <a href="{% url 'blog:post_create' %}" class="btn btn-primary">
            <i class="bi bi-plus-circle"></i> New Post
        </a>
    {% endif %}
{% else %}
    <a href="{% url 'accounts:login' %}" class="btn btn-outline-primary">
        Login to Create Posts
    </a>
{% endif %}
```

## Common Customizations

### 1. Change Color Scheme
Edit `/static/css/style.css`:
```css
:root {
    --primary-color: #yourcolor;
    --secondary-color: #yourcolor;
}
```

### 2. Modify Card Hover Effect
```css
.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0,0,0,.15);
}
```

### 3. Custom Font
Add to base.html `<head>`:
```html
<link href="https://fonts.googleapis.com/css2?family=Your+Font&display=swap" rel="stylesheet">
```

Then in style.css:
```css
body {
    font-family: 'Your Font', sans-serif;
}
```

### 4. Add Dark Mode Toggle
Add to base.html before `</body>`:
```html
<button id="darkModeToggle" class="btn btn-secondary">
    <i class="bi bi-moon-fill"></i>
</button>

<script>
    // Dark mode toggle logic
</script>
```

## Troubleshooting

### Images Not Displaying
1. Check `MEDIA_URL` and `MEDIA_ROOT` in settings
2. Ensure media URL patterns are added in development
3. Verify file upload permissions on `media/` directory
4. Check that `{% load static %}` is in template

### Static Files Not Loading
1. Run `python manage.py collectstatic`
2. Check `STATIC_URL` and `STATIC_ROOT` settings
3. Clear browser cache
4. Verify `{% load static %}` is used

### Forms Not Rendering Properly
1. Ensure Bootstrap classes are applied
2. Check form field widget in forms.py
3. Verify CSRF token is present
4. Check for JavaScript console errors

### Pagination Not Working
1. Verify view uses `ListView` or `Paginator`
2. Check `paginate_by` attribute in view
3. Ensure `page_obj` and `is_paginated` are in context

## Best Practices

1. **Always use `{% load static %}` when referencing static files**
2. **Use `get_full_name|default:username` for displaying user names**
3. **Add `alt` attributes to all images**
4. **Use `truncatewords` for excerpts to maintain layout**
5. **Include `striptags` when displaying rich text excerpts**
6. **Use `|safe` filter only for trusted HTML content**
7. **Add confirmation dialogs for destructive actions**
8. **Keep consistent spacing with Bootstrap utility classes**
9. **Use semantic HTML5 tags (article, nav, section, etc.)**
10. **Test on mobile devices and different screen sizes**
