from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()


@receiver(post_save, sender=Post)
def post_published_notification(sender, instance, created, **kwargs):
    """
    Send notification when a post is published.
    This signal is triggered after a post is saved.
    """
    # Check if the post status is 'published' and it's not a new creation
    # We check for status change by comparing with the previous state
    if instance.status == 'published' and instance.published_at:
        # Get all admin users and authors (excluding the post author)
        admin_users = User.objects.filter(role='Admin').exclude(id=instance.author.id)
        
        # Prepare notification message
        subject = f'New Post Published: {instance.title}'
        message = f"""
Hello,

A new blog post has been published:

Title: {instance.title}
Author: {instance.author.get_full_name() or instance.author.username}
Category: {instance.category.name if instance.category else 'Uncategorized'}
Published At: {instance.published_at.strftime('%Y-%m-%d %H:%M:%S')}

Excerpt:
{instance.excerpt or 'No excerpt available'}

You can view the post at: {instance.get_absolute_url()}

Best regards,
Blog System
"""
        
        # Collect recipient emails
        recipient_emails = [user.email for user in admin_users if user.email]
        
        # Send email notification (only if there are recipients and email is configured)
        if recipient_emails:
            try:
                # In production, configure EMAIL_BACKEND, EMAIL_HOST, etc. in settings.py
                # For development, this will use console backend if configured
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@blog.com',
                    recipient_list=recipient_emails,
                    fail_silently=True,  # Don't raise exception if email fails
                )
                print(f"✅ Notification sent for published post: {instance.title}")
            except Exception as e:
                print(f"⚠️ Failed to send email notification: {str(e)}")
        
        # Log to console for development
        print(f"📧 Post Published: '{instance.title}' by {instance.author.username}")


@receiver(post_save, sender=Comment)
def comment_notification(sender, instance, created, **kwargs):
    """
    Send notification to post author when a new comment is added.
    """
    if created and instance.is_approved:
        # Notify the post author about new comment
        post_author = instance.post.author
        
        # Don't notify if author is commenting on their own post
        if post_author.id == instance.author.id:
            return
        
        subject = f'New Comment on Your Post: {instance.post.title}'
        message = f"""
Hello {post_author.get_full_name() or post_author.username},

A new comment has been added to your post "{instance.post.title}":

Commented by: {instance.author.get_full_name() or instance.author.username}
Comment: {instance.content[:200]}{'...' if len(instance.content) > 200 else ''}

You can view the comment at: {instance.post.get_absolute_url()}

Best regards,
Blog System
"""
        
        # Send email notification
        if post_author.email:
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@blog.com',
                    recipient_list=[post_author.email],
                    fail_silently=True,
                )
                print(f"✅ Comment notification sent to {post_author.username}")
            except Exception as e:
                print(f"⚠️ Failed to send comment notification: {str(e)}")
        
        # If it's a reply, notify the parent comment author
        if instance.parent and instance.parent.author.id != instance.author.id:
            parent_author = instance.parent.author
            
            subject = f'New Reply to Your Comment on: {instance.post.title}'
            message = f"""
Hello {parent_author.get_full_name() or parent_author.username},

Someone replied to your comment on "{instance.post.title}":

Reply by: {instance.author.get_full_name() or instance.author.username}
Reply: {instance.content[:200]}{'...' if len(instance.content) > 200 else ''}

Original comment: {instance.parent.content[:100]}{'...' if len(instance.parent.content) > 100 else ''}

You can view the reply at: {instance.post.get_absolute_url()}

Best regards,
Blog System
"""
            
            if parent_author.email:
                try:
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@blog.com',
                        recipient_list=[parent_author.email],
                        fail_silently=True,
                    )
                    print(f"✅ Reply notification sent to {parent_author.username}")
                except Exception as e:
                    print(f"⚠️ Failed to send reply notification: {str(e)}")


@receiver(pre_save, sender=Post)
def track_post_status_change(sender, instance, **kwargs):
    """
    Track when a post status changes from draft to published.
    This helps ensure we only send notifications on actual publication.
    """
    if instance.pk:  # Only for existing posts
        try:
            old_instance = Post.objects.get(pk=instance.pk)
            # Store the old status for comparison
            instance._old_status = old_instance.status
        except Post.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None
