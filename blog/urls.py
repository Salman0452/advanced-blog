from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Post CRUD URLs
    path('', views.PostListView.as_view(), name='home'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/new/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/my-posts/', views.MyPostsListView.as_view(), name='my_posts'),
    path('posts/drafts/', views.DraftPostsListView.as_view(), name='draft_posts'),
    path('posts/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('posts/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # Draft/Published workflow URLs
    path('posts/<slug:slug>/publish/', views.PublishPostView.as_view(), name='post_publish'),
    path('posts/<slug:slug>/unpublish/', views.UnpublishPostView.as_view(), name='post_unpublish'),
    
    # Comment URLs
    path('posts/<slug:slug>/comment/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('comments/<int:pk>/moderate/', views.CommentModerateView.as_view(), name='comment_moderate'),
    path('comments/unapproved/', views.UnapprovedCommentsListView.as_view(), name='unapproved_comments'),
    
    # Search URL
    path('search/', views.PostSearchView.as_view(), name='post_search'),
    
    # Category URLs
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    
    # Tag URLs
    path('tags/', views.TagListView.as_view(), name='tag_list'),
    path('tag/<slug:slug>/', views.TagDetailView.as_view(), name='tag_detail'),
]
