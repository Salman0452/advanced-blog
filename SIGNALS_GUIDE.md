# Signals and Notifications System

This document explains the Django signals implementation for automatic notifications in the Advanced Django Blog.

## Overview

The blog uses Django signals to automatically send email notifications when certain events occur. This provides real-time communication to users about important activities.

## Signal Types Implemented

### 1. Post Publication Notification

**Trigger**: When a post status changes to 'published'

**Recipients**: All Admin users (except the post author)

**Signal**: `post_save` on Post model

**Implementation**: `blog/signals.py`

#### What Happens
```python
@receiver(post_save, sender=Post)
def post_published_notification(sender, instance, created, **kwargs):
    if instance.status == 'published' and instance.published_at:
        # Notify admin users about new publication
```

#### Notification Contains
- Post title
- Author name
- Category
- Published date/time
- Excerpt
- Link to view the post

#### Example Email
```
Subject: New Post Published: Introduction to Django Signals

Hello,

A new blog post has been published:

Title: Introduction to Django Signals
Author: John Doe
Category: Technology
Published At: 2025-11-16 14:30:00

Excerpt:
Learn how to use Django signals to automate your application...

You can view the post at: http://yourdomain.com/post/introduction-to-django-signals/

Best regards,
Blog System
```

### 2. New Comment Notification

**Trigger**: When a new comment is created and approved

**Recipients**: Post author (if not commenting on own post)

**Signal**: `post_save` on Comment model

**Implementation**: `blog/signals.py`

#### What Happens
```python
@receiver(post_save, sender=Comment)
def comment_notification(sender, instance, created, **kwargs):
    if created and instance.is_approved:
        # Notify post author about new comment
```

#### Notification Contains
- Post title
- Commenter name
- Comment content (first 200 characters)
- Link to view comment

#### Example Email
```
Subject: New Comment on Your Post: Introduction to Django Signals

Hello John Doe,

A new comment has been added to your post "Introduction to Django Signals":

Commented by: Jane Smith
Comment: Great article! I learned a lot about Django signals. Could you explain more about...

You can view the comment at: http://yourdomain.com/post/introduction-to-django-signals/

Best regards,
Blog System
```

### 3. Comment Reply Notification

**Trigger**: When someone replies to a comment

**Recipients**: Parent comment author (if different from reply author)

**Signal**: Part of `post_save` on Comment model

#### What Happens
```python
if instance.parent and instance.parent.author.id != instance.author.id:
    # Notify parent comment author about reply
```

#### Notification Contains
- Post title
- Replier name
- Reply content (first 200 characters)
- Original comment excerpt
- Link to view reply

#### Example Email
```
Subject: New Reply to Your Comment on: Introduction to Django Signals

Hello Jane Smith,

Someone replied to your comment on "Introduction to Django Signals":

Reply by: Mike Johnson
Reply: @Jane Thanks for your question! Let me explain the difference between...

Original comment: Great article! I learned a lot about Django signals. Could you explain...

You can view the reply at: http://yourdomain.com/post/introduction-to-django-signals/

Best regards,
Blog System
```

### 4. Post Status Tracking

**Trigger**: Before a post is saved

**Purpose**: Track status changes to determine if notification is needed

**Signal**: `pre_save` on Post model

#### What Happens
```python
@receiver(pre_save, sender=Post)
def track_post_status_change(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Post.objects.get(pk=instance.pk)
        instance._old_status = old_instance.status
```

This helps ensure notifications are only sent when a post transitions to 'published' status, not every time a published post is updated.

## Configuration

### Email Backend Configuration

**Development** (`settings.py`):
```python
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
- Emails printed to console
- No SMTP configuration needed
- Perfect for testing

**Production** (`settings.py`):
```python
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
    EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
```

### Environment Variables

Add to `.env` file:
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourblog.com
```

### Gmail Setup

1. Enable 2-Factor Authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use App Password in `EMAIL_HOST_PASSWORD`

### Alternative Email Providers

**SendGrid**:
```env
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
```

**Mailgun**:
```env
EMAIL_HOST=smtp.mailgun.org
EMAIL_PORT=587
EMAIL_HOST_USER=postmaster@yourdomain.mailgun.org
EMAIL_HOST_PASSWORD=your-mailgun-password
```

**Amazon SES**:
```env
EMAIL_HOST=email-smtp.us-east-1.amazonaws.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-ses-smtp-username
EMAIL_HOST_PASSWORD=your-ses-smtp-password
```

## Signal Registration

Signals are automatically registered when the blog app is ready.

**blog/apps.py**:
```python
class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    
    def ready(self):
        import blog.signals  # noqa
```

This ensures signals are connected when Django starts.

## Testing Notifications

### Test in Development

1. **Start development server**:
   ```bash
   python manage.py runserver
   ```

2. **Create a post and publish it**:
   - Login to admin
   - Create a new post
   - Set status to "Published"
   - Save

3. **Check console output**:
   - You'll see the email content printed to console
   - Example output:
     ```
     Content-Type: text/plain; charset="utf-8"
     MIME-Version: 1.0
     Content-Transfer-Encoding: 7bit
     Subject: New Post Published: Test Post
     From: noreply@blog.com
     To: admin@example.com
     Date: Sat, 16 Nov 2025 14:30:00 -0000
     
     Hello,
     
     A new blog post has been published:
     ...
     ```

4. **Test comment notifications**:
   - Add a comment to a post
   - Check console for notification email

### Test in Production

1. **Configure email settings** in `.env`

2. **Publish a post** or **add a comment**

3. **Check email inbox** of recipient

4. **Check logs** for any errors:
   ```bash
   # Heroku
   heroku logs --tail
   
   # PythonAnywhere
   # Check error log in Web tab
   
   # VPS
   sudo journalctl -u gunicorn -f
   ```

## Troubleshooting

### Notifications Not Sending

**Check 1: Email Backend**
```python
# In settings.py or Django shell
from django.conf import settings
print(settings.EMAIL_BACKEND)
```

**Check 2: Email Configuration**
```python
# Django shell
from django.core.mail import send_mail
send_mail(
    'Test Subject',
    'Test Message',
    'from@example.com',
    ['to@example.com'],
)
```

**Check 3: Recipient Emails**
```python
# Django shell
from accounts.models import User
admins = User.objects.filter(role='Admin')
for admin in admins:
    print(f"{admin.username}: {admin.email}")
```

**Check 4: Signal Registration**
```python
# Django shell
from django.db.models import signals
from blog.models import Post
print(signals.post_save.receivers)
```

### Common Issues

**Problem**: No emails sent in development
- **Solution**: Check console output, emails should be printed there

**Problem**: Gmail authentication fails
- **Solution**: Use App Password, not regular password

**Problem**: Emails go to spam
- **Solution**: Configure SPF/DKIM records for your domain

**Problem**: Signal fires too often
- **Solution**: Check status tracking logic in `pre_save` signal

**Problem**: Notification sent to post author
- **Solution**: Check author exclusion logic in signal

## Extending the Signal System

### Add New Signal

Create a new signal in `blog/signals.py`:

```python
@receiver(post_save, sender=YourModel)
def your_notification(sender, instance, created, **kwargs):
    if created:
        # Your notification logic
        subject = 'Your Subject'
        message = 'Your Message'
        recipient_list = ['email@example.com']
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=True,
        )
```

### Disable Specific Notifications

Temporarily disable a signal:

```python
# In views or management commands
from django.db.models.signals import post_save
from blog.models import Post
from blog.signals import post_published_notification

# Disconnect
post_save.disconnect(post_published_notification, sender=Post)

# Your code here

# Reconnect
post_save.connect(post_published_notification, sender=Post)
```

### Add HTML Email Templates

Enhance notifications with HTML:

```python
from django.core.mail import EmailMultiAlternatives

subject = 'Subject'
text_content = 'Plain text message'
html_content = '<h1>HTML message</h1>'

msg = EmailMultiAlternatives(subject, text_content, from_email, to_list)
msg.attach_alternative(html_content, "text/html")
msg.send()
```

## Performance Considerations

### Async Email Sending (Optional)

For better performance, consider using Celery for async email sending:

```python
# tasks.py
from celery import shared_task

@shared_task
def send_notification_email(subject, message, recipient_list):
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

# In signals.py
send_notification_email.delay(subject, message, recipient_emails)
```

### Batch Notifications

For multiple recipients, use bulk email:

```python
from django.core.mail import send_mass_mail

messages = [
    (subject, message, from_email, [to1]),
    (subject, message, from_email, [to2]),
]
send_mass_mail(messages)
```

## Security Considerations

1. **Use environment variables** for email credentials
2. **Enable fail_silently=True** to prevent email errors from breaking the app
3. **Limit recipient lists** to prevent spam
4. **Validate email addresses** before sending
5. **Rate limit** notifications if needed
6. **Use TLS/SSL** for email transmission

## Related Files

- **blog/signals.py**: Signal definitions
- **blog/apps.py**: Signal registration
- **advanced_blog/settings.py**: Email configuration
- **.env.example**: Environment variable template

## Further Reading

- [Django Signals Documentation](https://docs.djangoproject.com/en/stable/topics/signals/)
- [Django Email Documentation](https://docs.djangoproject.com/en/stable/topics/email/)
- [Celery for Async Tasks](https://docs.celeryproject.org/)

---

**Automated notifications keep your users engaged! 📧**
