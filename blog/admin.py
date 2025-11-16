from django.contrib import admin
from .models import Category, Tag, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin configuration"""
    
    list_display = ['name', 'slug', 'get_post_count', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    
    def get_post_count(self, obj):
        """Return the number of posts in this category"""
        return obj.posts.count()
    get_post_count.short_description = 'Posts'
    get_post_count.admin_order_field = 'posts__count'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag admin configuration"""
    
    list_display = ['name', 'slug', 'get_post_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
    
    def get_post_count(self, obj):
        """Return the number of posts with this tag"""
        return obj.posts.count()
    get_post_count.short_description = 'Posts'
    get_post_count.admin_order_field = 'posts__count'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Post admin configuration"""
    
    list_display = ['title', 'author', 'category', 'status', 'get_comment_count', 'views_count', 'created_at', 'published_at']
    list_filter = ['status', 'category', 'tags', 'created_at', 'published_at', 'author']
    search_fields = ['title', 'content', 'excerpt', 'author__username', 'author__email']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    filter_horizontal = ['tags']
    readonly_fields = ['views_count', 'created_at', 'updated_at', 'slug']
    list_per_page = 25
    list_editable = ['status']
    
    actions = ['publish_posts', 'draft_posts', 'archive_posts']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category', 'status')
        }),
        ('Content', {
            'fields': ('content', 'excerpt', 'featured_image')
        }),
        ('Metadata', {
            'fields': ('tags', 'views_count', 'published_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_comment_count(self, obj):
        """Return the number of comments on this post"""
        return obj.comments.count()
    get_comment_count.short_description = 'Comments'
    get_comment_count.admin_order_field = 'comments__count'
    
    def publish_posts(self, request, queryset):
        """Publish selected posts"""
        from django.utils import timezone
        updated = 0
        for post in queryset:
            if post.status != 'published':
                post.status = 'published'
                if not post.published_at:
                    post.published_at = timezone.now()
                post.save()
                updated += 1
        self.message_user(request, f'{updated} post(s) published.')
    publish_posts.short_description = 'Publish selected posts'
    
    def draft_posts(self, request, queryset):
        """Set selected posts to draft"""
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} post(s) set to draft.')
    draft_posts.short_description = 'Set to draft'
    
    def archive_posts(self, request, queryset):
        """Archive selected posts"""
        updated = queryset.update(status='archived')
        self.message_user(request, f'{updated} post(s) archived.')
    archive_posts.short_description = 'Archive selected posts'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('author', 'category').prefetch_related('tags')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment admin configuration"""
    
    list_display = ['get_comment_preview', 'author', 'post', 'is_approved', 'is_reply', 'created_at']
    list_filter = ['is_approved', 'created_at', 'post']
    search_fields = ['content', 'author__username', 'author__email', 'post__title']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at', 'post', 'author', 'parent']
    list_per_page = 50
    list_editable = ['is_approved']
    
    actions = ['approve_comments', 'unapprove_comments', 'delete_selected_comments']
    
    fieldsets = (
        ('Comment Information', {
            'fields': ('post', 'author', 'parent', 'content', 'is_approved')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_comment_preview(self, obj):
        """Return truncated comment content"""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    get_comment_preview.short_description = 'Content Preview'
    
    def approve_comments(self, request, queryset):
        """Approve selected comments"""
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} comment(s) approved.')
    approve_comments.short_description = 'Approve selected comments'
    
    def unapprove_comments(self, request, queryset):
        """Unapprove selected comments"""
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} comment(s) unapproved.')
    unapprove_comments.short_description = 'Unapprove selected comments'
    
    def delete_selected_comments(self, request, queryset):
        """Delete selected comments"""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} comment(s) deleted.')
    delete_selected_comments.short_description = 'Delete selected comments'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('author', 'post', 'parent')

