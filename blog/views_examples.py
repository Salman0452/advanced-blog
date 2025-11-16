"""
Example Blog Views with Permission Mixins
This file demonstrates how to use the custom permission mixins for role-based access control
"""

from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.contrib import messages
from accounts.permissions import (
    AdminRequiredMixin,
    AuthorRequiredMixin,
    AuthorOwnerRequiredMixin,
    ReaderRequiredMixin,
    CommentOwnerRequiredMixin
)
from .models import Post, Comment


# ============================================
# POST VIEWS
# ============================================

class PostListView(ListView):
    """
    Public view - anyone can see published posts
    No permission mixin required
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        # Only show published posts to non-authenticated users
        if self.request.user.is_authenticated and (
            self.request.user.is_admin() or self.request.user.is_author()
        ):
            return Post.objects.all().select_related('author', 'category')
        return Post.objects.filter(status='published').select_related('author', 'category')


class PostDetailView(DetailView):
    """
    Public view - anyone can read a post
    No permission mixin required
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_object(self):
        obj = super().get_object()
        # Increment view count
        obj.increment_views()
        return obj


class PostCreateView(AuthorRequiredMixin, CreateView):
    """
    Authors and Admins can create posts
    Uses AuthorRequiredMixin
    """
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'excerpt', 'category', 'tags', 'featured_image', 'status']
    
    def form_valid(self, form):
        # Automatically set the author to current user
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)


class PostUpdateView(AuthorOwnerRequiredMixin, UpdateView):
    """
    Only the post owner or Admin can edit a post
    Uses AuthorOwnerRequiredMixin to check ownership
    """
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'excerpt', 'category', 'tags', 'featured_image', 'status']
    
    def form_valid(self, form):
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)


class PostDeleteView(AuthorOwnerRequiredMixin, DeleteView):
    """
    Only the post owner or Admin can delete a post
    Uses AuthorOwnerRequiredMixin to check ownership
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ============================================
# COMMENT VIEWS
# ============================================

class CommentCreateView(ReaderRequiredMixin, CreateView):
    """
    Any authenticated user can comment
    Uses ReaderRequiredMixin (all authenticated users)
    """
    model = Comment
    template_name = 'blog/comment_form.html'
    fields = ['content']
    
    def form_valid(self, form):
        # Set the author to current user
        form.instance.author = self.request.user
        # Set the post from URL parameter
        form.instance.post_id = self.kwargs['post_id']
        messages.success(self.request, 'Comment added successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'slug': self.object.post.slug})


class CommentUpdateView(CommentOwnerRequiredMixin, UpdateView):
    """
    Only the comment owner or Admin can edit a comment
    Uses CommentOwnerRequiredMixin to check ownership
    """
    model = Comment
    template_name = 'blog/comment_form.html'
    fields = ['content']
    
    def form_valid(self, form):
        messages.success(self.request, 'Comment updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'slug': self.object.post.slug})


class CommentDeleteView(CommentOwnerRequiredMixin, DeleteView):
    """
    Only the comment owner or Admin can delete a comment
    Uses CommentOwnerRequiredMixin to check ownership
    """
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Comment deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'slug': self.object.post.slug})


# ============================================
# ADMIN-ONLY VIEWS
# ============================================

class PostApprovalView(AdminRequiredMixin, ListView):
    """
    Admin-only view to approve/manage posts
    Uses AdminRequiredMixin for admin-only access
    """
    model = Post
    template_name = 'blog/post_approval.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        # Show all draft posts waiting for approval
        return Post.objects.filter(status='draft').select_related('author', 'category')


class CommentModerationView(AdminRequiredMixin, ListView):
    """
    Admin-only view to moderate comments
    Uses AdminRequiredMixin for admin-only access
    """
    model = Comment
    template_name = 'blog/comment_moderation.html'
    context_object_name = 'comments'
    
    def get_queryset(self):
        # Show unapproved comments
        return Comment.objects.filter(is_approved=False).select_related('author', 'post')


# ============================================
# AUTHOR DASHBOARD
# ============================================

class AuthorDashboardView(AuthorRequiredMixin, ListView):
    """
    Authors can see their own posts
    Admins can see all posts
    Uses AuthorRequiredMixin
    """
    model = Post
    template_name = 'blog/author_dashboard.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        # Admins see all posts, Authors see only their own
        if self.request.user.is_admin():
            return Post.objects.all().select_related('author', 'category')
        return Post.objects.filter(author=self.request.user).select_related('category')


# ============================================
# PERMISSION MIXIN USAGE SUMMARY
# ============================================

"""
MIXIN HIERARCHY:

1. No Mixin (Public)
   - Anyone can access (including anonymous users)
   - Use for: Post list, Post detail, Static pages

2. ReaderRequiredMixin
   - Any authenticated user can access
   - Use for: Creating comments, Viewing profile, Basic features

3. AuthorRequiredMixin
   - Authors and Admins can access
   - Use for: Creating posts, Author dashboard

4. AuthorOwnerRequiredMixin
   - Post owner or Admin can access
   - Use for: Editing/deleting own posts
   - Automatically checks if user owns the object

5. CommentOwnerRequiredMixin
   - Comment owner or Admin can access
   - Use for: Editing/deleting own comments
   - Automatically checks if user owns the comment

6. AdminRequiredMixin
   - Only Admins can access
   - Use for: Post approval, Comment moderation, User management

BEST PRACTICES:

1. Always use the most restrictive mixin appropriate for the view
2. Admins automatically bypass owner checks in Owner mixins
3. Mixins handle authentication redirect automatically
4. Custom error messages are displayed via Django messages framework
5. Combine with get_queryset() to filter data based on user role

EXAMPLE URL PATTERNS:

from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Public views
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    
    # Author views
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('dashboard/', views.AuthorDashboardView.as_view(), name='author_dashboard'),
    
    # Reader views (comments)
    path('post/<int:post_id>/comment/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    
    # Admin views
    path('admin/posts/approval/', views.PostApprovalView.as_view(), name='post_approval'),
    path('admin/comments/moderate/', views.CommentModerationView.as_view(), name='comment_moderation'),
]
"""
