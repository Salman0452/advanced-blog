from django import forms
from .models import Post, Comment, Category, Tag
from ckeditor.widgets import CKEditorWidget


class PostForm(forms.ModelForm):
    """Form for creating and editing blog posts"""
    
    content = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'excerpt', 'category', 'tags', 'status', 'featured_image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description of the post (optional)'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tags': forms.CheckboxSelectMultiple(),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
        help_texts = {
            'title': 'Enter a descriptive title for your post',
            'excerpt': 'This will be shown in post listings',
            'tags': 'Select one or more tags',
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Make category optional
        self.fields['category'].required = False
        
        # If user is not an admin, limit status choices
        if self.user and not (self.user.is_admin() or self.user.is_superuser):
            self.fields['status'].choices = [
                ('draft', 'Draft'),
                ('published', 'Published'),
            ]


class CommentForm(forms.ModelForm):
    """Form for creating and editing comments"""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment here...'
            }),
        }
        labels = {
            'content': 'Comment',
        }


class PostSearchForm(forms.Form):
    """Form for searching blog posts"""
    
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search posts...',
        }),
        label='Search'
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='All Categories',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    tag = forms.ModelChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        empty_label='All Tags',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    status = forms.ChoiceField(
        choices=[('', 'All'), ('published', 'Published'), ('draft', 'Draft')],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )


class CommentModerationForm(forms.ModelForm):
    """Form for moderating comments"""
    
    class Meta:
        model = Comment
        fields = ['is_approved']
        widgets = {
            'is_approved': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
