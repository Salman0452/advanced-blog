from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Extended User model with role field"""
    
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Author', 'Author'),
        ('Reader', 'Reader'),
    ]
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='Reader',
        help_text='User role in the blog system'
    )
    bio = models.TextField(blank=True, null=True, help_text='User biography')
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        help_text='User profile picture'
    )
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.username} ({self.role})"
    
    def is_admin(self):
        return self.role == 'Admin'
    
    def is_author(self):
        return self.role == 'Author'
    
    def is_reader(self):
        return self.role == 'Reader'
