# Blog Features Quick Start Guide

## Initial Setup

### 1. Populate Sample Data (Optional)
After creating users with different roles, populate the blog with sample data:

```bash
python manage.py populate_blog
```

This creates:
- 5 categories
- 10 tags
- 5 sample posts (4 published, 1 draft)
- Sample comments on published posts

### 2. Create Users with Different Roles

**Option A: Using Django Admin**
1. Go to http://localhost:8000/admin/
2. Log in with superuser credentials
3. Add users under "Users" section
4. Assign roles: Admin, Author, or Reader

**Option B: Using Registration**
1. Go to http://localhost:8000/accounts/register/
2. Register a new account
3. Admin must approve and assign role via admin panel

## Using Blog Features

### For Readers

**What you can do:**
- ✅ Browse all published posts
- ✅ Search posts by keywords
- ✅ Filter by categories and tags
- ✅ Read post content
- ✅ Add comments on posts
- ✅ Delete your own comments

**Key URLs:**
- Home/Post List: `/`
- Search Posts: `/search/`
- Categories: `/categories/`
- Tags: `/tags/`

### For Authors

**Everything Readers can do, PLUS:**
- ✅ Create new blog posts
- ✅ Edit your own posts
- ✅ Delete your own posts
- ✅ Manage drafts
- ✅ Publish/unpublish your posts
- ✅ Add featured images
- ✅ Categorize and tag posts

**Key URLs:**
- Create Post: `/posts/new/`
- My Posts: `/posts/my-posts/`
- My Drafts: `/posts/drafts/`

**Workflow:**
1. Click "New Post" in navigation
2. Fill in title, content, category, tags
3. Choose status: Draft or Published
4. Save post
5. From "My Posts", manage all your content

### For Admins

**Everything Authors can do, PLUS:**
- ✅ Edit ANY post
- ✅ Delete ANY post
- ✅ Publish/unpublish ANY post
- ✅ Moderate comments (approve/unapprove)
- ✅ Delete any comment
- ✅ View all drafts from all authors
- ✅ Access Django admin panel

**Key URLs:**
- All Drafts: `/posts/drafts/`
- Moderate Comments: `/comments/unapproved/`
- Admin Panel: `/admin/`

## Features Guide

### Creating a Post

1. Navigate to `/posts/new/` or click "New Post"
2. Enter required fields:
   - **Title**: Post headline (required)
   - **Content**: Rich text content (required)
   - **Excerpt**: Brief description (optional, auto-generated from content if empty)
3. Optional fields:
   - **Category**: Select from dropdown
   - **Tags**: Check multiple tags
   - **Featured Image**: Upload image
4. Choose **Status**:
   - **Draft**: Save for later, not visible to public
   - **Published**: Immediately visible to all users
5. Click "Create Post"

### Draft/Published Workflow

**Creating Draft:**
- Set status to "Draft" when creating post
- Draft visible only to you (and Admins)
- Continue editing until ready

**Publishing Draft:**
1. Go to "My Drafts" or "My Posts"
2. Click post to view
3. Click "Publish" button
4. Confirm publication
5. Post now visible to all users with timestamp

**Unpublishing Post:**
1. View published post
2. Click "Unpublish" button
3. Confirm action
4. Post converted back to draft

### Managing Comments

**Adding Comment:**
1. View any published post
2. Scroll to comments section
3. Type comment in text box
4. Click "Post Comment"

**Deleting Comment:**
- Your own comments: Click trash icon next to comment
- Any comment (Admin only): Click trash icon

**Moderating Comments (Admin):**
1. Go to `/comments/unapproved/`
2. View all pending comments
3. Click "Moderate" on any comment
4. Check/uncheck "Approve" checkbox
5. Click "Update Status"

### Using Search

**Basic Search:**
1. Go to `/search/` or use search box on home
2. Enter keywords
3. Press "Search"

**Advanced Search:**
1. Go to `/search/`
2. Enter keywords (searches title, content, excerpt, author)
3. Select category filter (optional)
4. Select tag filter (optional)
5. For authenticated users: filter by status
6. Click "Search"

**Search Tips:**
- Searches across post title, content, excerpt
- Also searches author names
- Combine filters for precise results
- Results paginated (10 per page)

### Filtering by Category/Tag

**By Category:**
1. Go to `/categories/` to see all
2. Click any category
3. View all posts in that category
4. Pagination available

**By Tag:**
1. Go to `/tags/` to see all
2. Click any tag
3. View all posts with that tag
4. Pagination available

**Quick Filter:**
- Click category badge on any post
- Click tag badge on any post
- Sidebar widgets on home page

### Viewing Posts

**Post List View:**
- Shows post title, excerpt, author
- Category and tags
- View count, comment count
- Publication date
- Featured image (if set)
- Paginated (10 per page)

**Post Detail View:**
- Full content with rich text
- Author information
- Category and tags
- All approved comments
- Comment form (if logged in)
- Edit/Delete buttons (if you own post or are Admin)

## URL Reference

### Public URLs
- `/` - Home (published posts)
- `/posts/` - Post list
- `/posts/<slug>/` - Post detail
- `/search/` - Search posts
- `/categories/` - List categories
- `/category/<slug>/` - Posts by category
- `/tags/` - List tags  
- `/tag/<slug>/` - Posts by tag

### Author URLs (Requires Author/Admin role)
- `/posts/new/` - Create post
- `/posts/my-posts/` - My posts
- `/posts/drafts/` - Draft posts
- `/posts/<slug>/edit/` - Edit post
- `/posts/<slug>/delete/` - Delete post
- `/posts/<slug>/publish/` - Publish draft
- `/posts/<slug>/unpublish/` - Unpublish post

### Comment URLs (Login required)
- `/posts/<slug>/comment/` - Add comment
- `/comments/<id>/delete/` - Delete comment

### Admin URLs (Admin role only)
- `/comments/unapproved/` - Unapproved comments
- `/comments/<id>/moderate/` - Moderate comment
- `/admin/` - Django admin panel

## Tips & Best Practices

### For Authors

1. **Use Drafts**: Write posts as drafts, review, then publish
2. **Add Excerpts**: Write compelling excerpts for better previews
3. **Categorize**: Always assign a category for better organization
4. **Tag Appropriately**: Use 2-5 relevant tags per post
5. **Featured Images**: Add images for visual appeal
6. **Review Before Publishing**: Check formatting and content
7. **Engage**: Respond to comments on your posts

### For SEO & Engagement

1. **Descriptive Titles**: Use clear, keyword-rich titles
2. **Quality Content**: Write valuable, well-formatted content
3. **Internal Linking**: Reference related posts
4. **Consistent Publishing**: Regular content schedule
5. **Tag Strategy**: Use consistent, meaningful tags
6. **Category Structure**: Maintain clear category hierarchy

### For Admins

1. **Monitor Comments**: Regularly check unapproved comments
2. **Quality Control**: Review drafts before major publishing
3. **Category Management**: Keep categories organized via admin
4. **Tag Cleanup**: Merge similar tags periodically
5. **User Management**: Assign appropriate roles
6. **Content Guidelines**: Establish clear posting guidelines

## Troubleshooting

### Cannot Create Post
- **Check Role**: Must be Author or Admin
- **Check Login**: Must be authenticated
- **Check Required Fields**: Title and content are required

### Post Not Visible
- **Check Status**: Must be "Published" to be public
- **Check Published Date**: Auto-set when publishing

### Comment Not Showing
- **Check Approval**: Comments must be approved (default is approved)
- **Check Login**: Must be logged in to see comment form

### Cannot Edit Post
- **Check Ownership**: Must be post owner or Admin
- **Check Role**: Must be Author or Admin

### Search No Results
- **Check Spelling**: Try different keywords
- **Remove Filters**: Clear category/tag filters
- **Check Status**: May be searching drafts (authenticated only)

## Admin Panel Features

Access at `/admin/` with Admin credentials:

### Posts Management
- List all posts with filters
- Bulk status changes
- Direct edit access
- View counts visible

### Categories
- Add/edit categories
- Set descriptions
- Auto-generate slugs

### Tags
- Add/edit tags
- Merge similar tags
- Auto-generate slugs

### Comments
- List all comments
- Filter by approval status
- Bulk approve/unapprove
- Quick content preview

## Performance Tips

1. **Database**: Migrations already include indexes
2. **Images**: Optimize images before upload
3. **Caching**: Consider caching for high-traffic sites
4. **Pagination**: Default 10 items per page
5. **Query Optimization**: Already using select_related/prefetch_related

## Security Notes

1. **Permissions**: Enforced at view level
2. **CSRF Protection**: Enabled on all forms
3. **XSS Protection**: Content sanitized
4. **Authentication**: Required for protected actions
5. **Authorization**: Role-based access control

## Next Steps

1. Customize templates to match your brand
2. Add custom CSS in `/static/css/style.css`
3. Configure email notifications (optional)
4. Set up production deployment
5. Enable caching for performance
6. Add analytics tracking
7. Configure SEO meta tags
8. Set up automated backups
