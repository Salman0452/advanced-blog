from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from blog.models import Category, Tag, Post, Comment
from django.utils.text import slugify
from django.utils import timezone

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the database with sample blog data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting to populate sample data...'))

        # Create categories
        categories_data = [
            {'name': 'Technology', 'description': 'Latest tech news and tutorials'},
            {'name': 'Programming', 'description': 'Coding tips and best practices'},
            {'name': 'Web Development', 'description': 'Web development guides and resources'},
            {'name': 'Data Science', 'description': 'Data analysis and machine learning'},
            {'name': 'Mobile Development', 'description': 'iOS and Android development'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create tags
        tags_data = ['Python', 'Django', 'JavaScript', 'React', 'Vue', 'Node.js', 
                     'Machine Learning', 'AI', 'Tutorial', 'Best Practices']

        tags = {}
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags[tag_name] = tag
            if created:
                self.stdout.write(f'Created tag: {tag.name}')

        # Get or create sample users (ensure they exist)
        try:
            admin = User.objects.get(role='Admin')
        except User.DoesNotExist:
            self.stdout.write(self.style.WARNING('No Admin user found. Please create one first.'))
            admin = None

        try:
            author = User.objects.filter(role='Author').first()
        except User.DoesNotExist:
            self.stdout.write(self.style.WARNING('No Author user found. Please create one first.'))
            author = None

        if not admin and not author:
            self.stdout.write(self.style.ERROR('No users found. Please create Admin and/or Author users first.'))
            return

        # Use whichever user is available
        post_author = author if author else admin

        # Create sample posts
        posts_data = [
            {
                'title': 'Getting Started with Django',
                'content': '<h2>Introduction to Django</h2><p>Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. In this tutorial, we\'ll cover the basics of getting started with Django.</p><h3>Installation</h3><p>First, install Django using pip:</p><pre>pip install django</pre><h3>Creating Your First Project</h3><p>Create a new Django project with:</p><pre>django-admin startproject myproject</pre>',
                'excerpt': 'Learn how to get started with Django, the Python web framework.',
                'category': categories['Programming'],
                'tags': [tags['Python'], tags['Django'], tags['Tutorial']],
                'status': 'published',
            },
            {
                'title': 'Building RESTful APIs with Django REST Framework',
                'content': '<h2>Django REST Framework</h2><p>Django REST Framework (DRF) is a powerful toolkit for building Web APIs. It provides features like serialization, authentication, and browsable API interface.</p><h3>Key Features</h3><ul><li>Serialization that supports both ORM and non-ORM data sources</li><li>Fully customizable</li><li>Extensive documentation</li></ul>',
                'excerpt': 'A comprehensive guide to building APIs with Django REST Framework.',
                'category': categories['Web Development'],
                'tags': [tags['Python'], tags['Django'], tags['Best Practices']],
                'status': 'published',
            },
            {
                'title': 'Introduction to Machine Learning with Python',
                'content': '<h2>Machine Learning Basics</h2><p>Machine Learning is a subset of artificial intelligence that provides systems the ability to automatically learn and improve from experience.</p><h3>Popular Libraries</h3><ul><li>Scikit-learn</li><li>TensorFlow</li><li>PyTorch</li></ul>',
                'excerpt': 'Dive into the world of machine learning with Python.',
                'category': categories['Data Science'],
                'tags': [tags['Python'], tags['Machine Learning'], tags['AI'], tags['Tutorial']],
                'status': 'published',
            },
            {
                'title': 'Modern JavaScript ES6+ Features',
                'content': '<h2>ES6 and Beyond</h2><p>ECMAScript 6 introduced many new features that make JavaScript more powerful and expressive.</p><h3>Key Features</h3><ul><li>Arrow functions</li><li>Template literals</li><li>Destructuring</li><li>Promises and async/await</li></ul>',
                'excerpt': 'Explore the latest features in modern JavaScript.',
                'category': categories['Programming'],
                'tags': [tags['JavaScript'], tags['Tutorial']],
                'status': 'published',
            },
            {
                'title': 'Building Mobile Apps with React Native',
                'content': '<h2>React Native Development</h2><p>React Native allows you to build mobile applications using JavaScript and React. Write once, run on both iOS and Android.</p>',
                'excerpt': 'Learn how to build cross-platform mobile apps with React Native.',
                'category': categories['Mobile Development'],
                'tags': [tags['JavaScript'], tags['React']],
                'status': 'draft',
            },
        ]

        created_posts = []
        for post_data in posts_data:
            tags_list = post_data.pop('tags')
            post, created = Post.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    'author': post_author,
                    'content': post_data['content'],
                    'excerpt': post_data['excerpt'],
                    'category': post_data['category'],
                    'status': post_data['status'],
                    'published_at': timezone.now() if post_data['status'] == 'published' else None,
                }
            )
            if created:
                post.tags.set(tags_list)
                created_posts.append(post)
                self.stdout.write(f'Created post: {post.title}')

        # Create sample comments (only on published posts)
        if created_posts:
            try:
                reader = User.objects.filter(role='Reader').first()
                if not reader:
                    reader = post_author
            except User.DoesNotExist:
                reader = post_author

            comments_data = [
                'Great tutorial! Very helpful for beginners.',
                'Thanks for sharing this. I learned a lot.',
                'Could you add more examples?',
                'This is exactly what I was looking for!',
                'Well written and easy to follow.',
            ]

            for post in created_posts[:3]:  # Add comments to first 3 posts
                if post.status == 'published':
                    for i, comment_text in enumerate(comments_data[:2]):
                        comment, created = Comment.objects.get_or_create(
                            post=post,
                            author=reader if i % 2 == 0 else post_author,
                            content=comment_text,
                            defaults={'is_approved': True}
                        )
                        if created:
                            self.stdout.write(f'Created comment on: {post.title}')

        self.stdout.write(self.style.SUCCESS('Successfully populated sample data!'))
        self.stdout.write(f'Created {Category.objects.count()} categories')
        self.stdout.write(f'Created {Tag.objects.count()} tags')
        self.stdout.write(f'Created {Post.objects.count()} posts')
        self.stdout.write(f'Created {Comment.objects.count()} comments')
