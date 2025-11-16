from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin with role field"""
    
    list_display = ['username', 'email', 'role', 'first_name', 'last_name', 'is_staff', 'is_active', 'get_post_count', 'date_joined']
    list_filter = ['role', 'is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    list_per_page = 25
    date_hierarchy = 'date_joined'
    
    actions = ['activate_users', 'deactivate_users', 'make_authors', 'make_readers']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'bio', 'profile_picture')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'email', 'first_name', 'last_name')
        }),
    )
    
    def get_post_count(self, obj):
        """Return the number of posts by this user"""
        return obj.posts.count()
    get_post_count.short_description = 'Posts'
    get_post_count.admin_order_field = 'posts__count'
    
    def activate_users(self, request, queryset):
        """Activate selected users"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} user(s) activated.')
    activate_users.short_description = 'Activate selected users'
    
    def deactivate_users(self, request, queryset):
        """Deactivate selected users"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} user(s) deactivated.')
    deactivate_users.short_description = 'Deactivate selected users'
    
    def make_authors(self, request, queryset):
        """Set selected users to Author role"""
        updated = queryset.update(role='Author')
        self.message_user(request, f'{updated} user(s) set to Author.')
    make_authors.short_description = 'Set role to Author'
    
    def make_readers(self, request, queryset):
        """Set selected users to Reader role"""
        updated = queryset.update(role='Reader')
        self.message_user(request, f'{updated} user(s) set to Reader.')
    make_readers.short_description = 'Set role to Reader'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related()

