from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.db.models import Q, Count
from django.utils import timezone
from django.http import JsonResponse, HttpResponseForbidden
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post, Comment, Category, Tag
from .forms import PostForm, CommentForm, PostSearchForm, CommentModerationForm
from accounts.permissions import (
    AuthorRequiredMixin, 
    AuthorOwnerRequiredMixin, 
    AdminRequiredMixin,
    ReaderRequiredMixin,
    CommentOwnerRequiredMixin
)


# ============================================================================
# POST VIEWS - CRUD Operations
# ============================================================================

class PostListView(ListView):
    """List all published posts with pagination"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Post.objects.filter(status='published').select_related(
            'author', 'category'
        ).prefetch_related('tags', 'comments')
        
        # Annotate with comment count
        queryset = queryset.annotate(comment_count=Count('comments'))
        
        return queryset.order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context


class PostDetailView(DetailView):
    """Display a single post with comments"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        queryset = Post.objects.select_related('author', 'category').prefetch_related('tags')
        
        # Only show published posts to non-authenticated users
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='published')
        # Authors can see their own drafts, admins can see all
        elif not (self.request.user.is_admin() or self.request.user.is_superuser):
            queryset = queryset.filter(
                Q(status='published') | Q(author=self.request.user)
            )
        
        return queryset
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Increment view count
        obj.increment_views()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        
        # Get approved comments for this post
        comments = post.comments.filter(
            is_approved=True, 
            parent__isnull=True
        ).select_related('author').prefetch_related('replies')
        
        context['comments'] = comments
        context['comment_form'] = CommentForm()
        
        # Check if user can edit this post
        if self.request.user.is_authenticated:
            context['can_edit'] = (
                post.author == self.request.user or 
                self.request.user.is_admin() or 
                self.request.user.is_superuser
            )
        else:
            context['can_edit'] = False
        
        return context


class PostCreateView(AuthorRequiredMixin, CreateView):
    """Create a new blog post - requires Author role"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:my_posts')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Create New Post'
        context['submit_text'] = 'Create Post'
        return context


class PostUpdateView(AuthorOwnerRequiredMixin, UpdateView):
    """Update an existing post - requires Author to be owner or Admin"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.object.slug})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Post'
        context['submit_text'] = 'Update Post'
        return context


class PostDeleteView(AuthorOwnerRequiredMixin, DeleteView):
    """Delete a post - requires Author to be owner or Admin"""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:my_posts')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)


class MyPostsListView(AuthorRequiredMixin, ListView):
    """List all posts by the current user"""
    model = Post
    template_name = 'blog/my_posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Post.objects.filter(author=self.request.user).select_related(
            'category'
        ).prefetch_related('tags')
        
        # Annotate with comment count
        queryset = queryset.annotate(comment_count=Count('comments'))
        
        return queryset.order_by('-created_at')


# ============================================================================
# DRAFT/PUBLISHED WORKFLOW VIEWS
# ============================================================================

class DraftPostsListView(AuthorRequiredMixin, ListView):
    """List all draft posts"""
    model = Post
    template_name = 'blog/draft_posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Post.objects.filter(status='draft')
        
        # Authors see only their drafts, Admins see all
        if not (self.request.user.is_admin() or self.request.user.is_superuser):
            queryset = queryset.filter(author=self.request.user)
        
        queryset = queryset.select_related('author', 'category').prefetch_related('tags')
        return queryset.order_by('-created_at')


class PublishPostView(AuthorOwnerRequiredMixin, UpdateView):
    """Publish a draft post"""
    model = Post
    fields = []
    template_name = 'blog/post_publish_confirm.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        # Only allow publishing drafts
        return Post.objects.filter(status='draft')
    
    def form_valid(self, form):
        self.object.status = 'published'
        self.object.published_at = timezone.now()
        self.object.save()
        messages.success(self.request, f'Post "{self.object.title}" has been published!')
        return redirect('blog:post_detail', slug=self.object.slug)


class UnpublishPostView(AuthorOwnerRequiredMixin, UpdateView):
    """Unpublish a post (convert to draft)"""
    model = Post
    fields = []
    template_name = 'blog/post_unpublish_confirm.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        # Only allow unpublishing published posts
        return Post.objects.filter(status='published')
    
    def form_valid(self, form):
        self.object.status = 'draft'
        self.object.save()
        messages.success(self.request, f'Post "{self.object.title}" has been unpublished!')
        return redirect('blog:my_posts')


# ============================================================================
# COMMENT VIEWS
# ============================================================================

class CommentCreateView(ReaderRequiredMixin, CreateView):
    """Create a comment on a post - requires authentication"""
    model = Comment
    form_class = CommentForm
    
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=kwargs['slug'])
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            
            # Handle parent comment for replies
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                comment.parent = parent_comment
            
            comment.save()
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Error adding comment. Please try again.')
        
        return redirect('blog:post_detail', slug=post.slug)


class CommentDeleteView(CommentOwnerRequiredMixin, DeleteView):
    """Delete a comment - requires comment owner or Admin"""
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.object.post.slug})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Comment deleted successfully!')
        return super().delete(request, *args, **kwargs)


class CommentModerateView(AdminRequiredMixin, UpdateView):
    """Moderate comment approval - Admin only"""
    model = Comment
    form_class = CommentModerationForm
    template_name = 'blog/comment_moderate.html'
    
    def form_valid(self, form):
        comment = form.save()
        status = 'approved' if comment.is_approved else 'unapproved'
        messages.success(self.request, f'Comment {status} successfully!')
        return redirect('blog:post_detail', slug=comment.post.slug)


class UnapprovedCommentsListView(AdminRequiredMixin, ListView):
    """List all unapproved comments - Admin only"""
    model = Comment
    template_name = 'blog/unapproved_comments.html'
    context_object_name = 'comments'
    paginate_by = 20
    
    def get_queryset(self):
        return Comment.objects.filter(is_approved=False).select_related(
            'author', 'post'
        ).order_by('-created_at')


# ============================================================================
# SEARCH FUNCTIONALITY
# ============================================================================

class PostSearchView(ListView):
    """Search posts using Q objects"""
    model = Post
    template_name = 'blog/post_search.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Post.objects.filter(status='published').select_related(
            'author', 'category'
        ).prefetch_related('tags')
        
        # Get search query
        query = self.request.GET.get('query', '').strip()
        
        if query:
            # Search in title, content, and excerpt using Q objects
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(excerpt__icontains=query) |
                Q(author__username__icontains=query) |
                Q(author__first_name__icontains=query) |
                Q(author__last_name__icontains=query)
            )
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        # Filter by tag
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__id=tag)
        
        # Filter by status (for authenticated users)
        status = self.request.GET.get('status')
        if status and self.request.user.is_authenticated:
            if self.request.user.is_admin() or self.request.user.is_superuser:
                queryset = Post.objects.filter(status=status)
            elif status == 'draft':
                queryset = Post.objects.filter(status='draft', author=self.request.user)
        
        # Annotate with comment count
        queryset = queryset.annotate(comment_count=Count('comments'))
        
        return queryset.distinct().order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = PostSearchForm(self.request.GET)
        context['query'] = self.request.GET.get('query', '')
        context['total_results'] = self.get_queryset().count()
        return context


# ============================================================================
# CATEGORY AND TAG FILTERING VIEWS
# ============================================================================

class CategoryDetailView(DetailView):
    """Display posts filtered by category"""
    model = Category
    template_name = 'blog/category_detail.html'
    context_object_name = 'category'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all published posts in this category
        posts = Post.objects.filter(
            category=self.object,
            status='published'
        ).select_related('author').prefetch_related('tags').annotate(
            comment_count=Count('comments')
        ).order_by('-published_at')
        
        # Paginate posts
        paginator = Paginator(posts, 10)
        page = self.request.GET.get('page')
        
        try:
            posts_page = paginator.page(page)
        except PageNotAnInteger:
            posts_page = paginator.page(1)
        except EmptyPage:
            posts_page = paginator.page(paginator.num_pages)
        
        context['posts'] = posts_page
        context['page_obj'] = posts_page
        context['is_paginated'] = posts_page.has_other_pages()
        
        return context


class TagDetailView(DetailView):
    """Display posts filtered by tag"""
    model = Tag
    template_name = 'blog/tag_detail.html'
    context_object_name = 'tag'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all published posts with this tag
        posts = Post.objects.filter(
            tags=self.object,
            status='published'
        ).select_related('author', 'category').prefetch_related('tags').annotate(
            comment_count=Count('comments')
        ).order_by('-published_at')
        
        # Paginate posts
        paginator = Paginator(posts, 10)
        page = self.request.GET.get('page')
        
        try:
            posts_page = paginator.page(page)
        except PageNotAnInteger:
            posts_page = paginator.page(1)
        except EmptyPage:
            posts_page = paginator.page(paginator.num_pages)
        
        context['posts'] = posts_page
        context['page_obj'] = posts_page
        context['is_paginated'] = posts_page.has_other_pages()
        
        return context


class CategoryListView(ListView):
    """List all categories"""
    model = Category
    template_name = 'blog/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.annotate(
            post_count=Count('posts', filter=Q(posts__status='published'))
        ).order_by('name')


class TagListView(ListView):
    """List all tags"""
    model = Tag
    template_name = 'blog/tag_list.html'
    context_object_name = 'tags'
    
    def get_queryset(self):
        return Tag.objects.annotate(
            post_count=Count('posts', filter=Q(posts__status='published'))
        ).order_by('name')

