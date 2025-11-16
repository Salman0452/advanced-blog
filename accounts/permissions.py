from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied


class RoleRequiredMixin(AccessMixin):
    """Base mixin for role-based access control"""
    
    allowed_roles = []
    permission_denied_message = "You don't have permission to access this page."
    redirect_url = 'blog:home'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please log in to access this page.')
            return self.handle_no_permission()
        
        if not self.has_permission():
            messages.error(request, self.permission_denied_message)
            return redirect(self.redirect_url)
        
        return super().dispatch(request, *args, **kwargs)
    
    def has_permission(self):
        """Check if user has the required role"""
        return self.request.user.role in self.allowed_roles


class AdminRequiredMixin(RoleRequiredMixin):
    """Mixin to require Admin role - Full access to all features"""
    
    allowed_roles = ['Admin']
    permission_denied_message = "Admin access required. Only administrators can access this page."
    
    def has_permission(self):
        """Admin has full access"""
        return self.request.user.is_admin() or self.request.user.is_superuser


class AuthorRequiredMixin(RoleRequiredMixin):
    """Mixin to require Author role - Can create and manage own posts"""
    
    allowed_roles = ['Admin', 'Author']
    permission_denied_message = "Author access required. You must be an Author to access this page."
    
    def has_permission(self):
        """Authors and Admins can access"""
        return self.request.user.is_author() or self.request.user.is_admin() or self.request.user.is_superuser


class AuthorOwnerRequiredMixin(AuthorRequiredMixin):
    """Mixin to require user to be the owner of the post or an Admin"""
    
    permission_denied_message = "You can only edit your own posts."
    
    def has_permission(self):
        """Check if user is the post owner or an admin"""
        if not super().has_permission():
            return False
        
        # Admin has access to all posts
        if self.request.user.is_admin() or self.request.user.is_superuser:
            return True
        
        # Check if object has author attribute and user is the owner
        obj = self.get_object() if hasattr(self, 'get_object') else None
        if obj and hasattr(obj, 'author'):
            return obj.author == self.request.user
        
        return False


class ReaderRequiredMixin(RoleRequiredMixin):
    """Mixin to require at least Reader role - Can comment on posts"""
    
    allowed_roles = ['Admin', 'Author', 'Reader']
    permission_denied_message = "You must be logged in to access this page."
    
    def has_permission(self):
        """All authenticated users can access"""
        return self.request.user.is_authenticated


class CommentOwnerRequiredMixin(ReaderRequiredMixin):
    """Mixin to require user to be the owner of the comment or an Admin"""
    
    permission_denied_message = "You can only edit or delete your own comments."
    
    def has_permission(self):
        """Check if user is the comment owner or an admin"""
        if not self.request.user.is_authenticated:
            return False
        
        # Admin has access to all comments
        if self.request.user.is_admin() or self.request.user.is_superuser:
            return True
        
        # Check if object has author attribute and user is the owner
        obj = self.get_object() if hasattr(self, 'get_object') else None
        if obj and hasattr(obj, 'author'):
            return obj.author == self.request.user
        
        return False
