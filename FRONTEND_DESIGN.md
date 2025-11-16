# Frontend Design Documentation

## Overview
This document describes the responsive frontend design and template structure for the Advanced Blog application.

## Tech Stack
- **CSS Framework**: Bootstrap 5.3.2
- **Icons**: Bootstrap Icons 1.11.1
- **Rich Text Editor**: CKEditor
- **Custom CSS**: `/static/css/style.css`

## Template Structure

### Base Template (`base.html`)
The foundation template that all other templates extend.

**Features:**
- Responsive navigation bar with dropdown menus
- Role-based user interface elements
- Flash message display system
- Mobile-friendly hamburger menu
- Footer with site information
- Bootstrap 5 and custom CSS integration

**Navigation Menu:**
- Home
- Categories
- Tags
- Search
- User dropdown (when authenticated):
  - Profile
  - My Posts (Authors/Admins)
  - My Drafts (Authors/Admins)
  - Create Post (Authors/Admins)
  - Moderate Comments (Admins)
  - Admin Panel (Admins)
  - Logout

### Blog Templates

#### 1. Home Page (`blog/home.html`)
**Purpose:** Landing page and dashboard

**Sections:**
- Welcome card with user information (if authenticated)
- User statistics (role, join date, email)
- Latest blog posts list with thumbnails
- Sidebar with:
  - User permissions card
  - Features list
  - User roles information

**Features:**
- Displays up to 5 latest published posts
- Shows featured images as thumbnails
- Category and tag badges
- Post metadata (author, date, views)
- Responsive grid layout

#### 2. Post List (`blog/post_list.html`)
**Purpose:** Display all published posts with pagination

**Features:**
- Search box for filtering posts
- Post cards with:
  - Featured images (300px height)
  - Title, author, date, views, comments count
  - Category and tag badges
  - Excerpt preview (50 words)
  - "Read More" button
- Sidebar with:
  - Categories widget
  - Popular tags widget
- Pagination controls
- "New Post" button for authors/admins

#### 3. Post Detail (`blog/post_detail.html`)
**Purpose:** Display full post content with comments

**Features:**
- Full-width featured image
- Post metadata bar
- Category and tag badges
- Rich text content display
- Post actions (Edit, Publish/Unpublish, Delete) for authorized users
- Comments section:
  - Comment form for authenticated users
  - Threaded replies support
  - User role badges on comments
  - Delete button for comment authors/admins
  - Timestamps for all comments
- Sidebar with:
  - Author information card
  - Related posts by category

#### 4. Post Form (`blog/post_form.html`)
**Purpose:** Create and edit posts

**Features:**
- Title input field
- CKEditor for rich text content
- Excerpt text area
- Category dropdown
- Status selector (draft/published/archived)
- Tag multi-select checkboxes
- Featured image upload
- Submit and Cancel buttons
- Form validation with error messages

#### 5. My Posts (`blog/my_posts.html`)
**Purpose:** Author dashboard to manage own posts

**Features:**
- Table view of all user's posts
- Columns: Title, Status, Category, Views, Comments, Created Date
- Action buttons for each post:
  - Edit
  - Publish/Unpublish
  - Delete
- Status badges (color-coded)
- Pagination
- "New Post" and "View Drafts" buttons

#### 6. Draft Posts (`blog/draft_posts.html`)
**Purpose:** View and manage draft posts

**Features:**
- Similar to My Posts but filtered for drafts only
- Quick publish functionality
- Draft count display

#### 7. Category List (`blog/category_list.html`)
**Purpose:** Browse all categories

**Features:**
- Grid layout (3 columns on desktop)
- Category cards with:
  - Category name
  - Description preview
  - Post count badge
  - "View Posts" button
- Hover effects on cards

#### 8. Category Detail (`blog/category_detail.html`)
**Purpose:** Display posts in a specific category

**Features:**
- Breadcrumb navigation
- Category header with description
- Post count
- Filtered post list
- Pagination

#### 9. Tag List (`blog/tag_list.html`)
**Purpose:** Browse all tags

**Features:**
- Tag cloud display
- Interactive tag buttons
- Post count badges
- Hover effects

#### 10. Tag Detail (`blog/tag_detail.html`)
**Purpose:** Display posts with a specific tag

**Features:**
- Breadcrumb navigation
- Tag header
- Post count
- Filtered post list
- Pagination

#### 11. Post Search (`blog/post_search.html`)
**Purpose:** Advanced search functionality

**Features:**
- Multi-field search form:
  - Text query
  - Category filter
  - Tag filter
  - Status filter (for authenticated users)
- Search results count
- Filtered post list
- Search tips sidebar
- Pagination with query preservation

### Authentication Templates

#### 1. Login (`accounts/login.html`)
**Purpose:** User authentication

**Features:**
- Username field
- Password field
- "Remember me" checkbox
- Error message display
- "Forgot password" link
- "Register" link
- Role information card
- Clean centered layout

#### 2. Register (`accounts/register.html`)
**Purpose:** New user registration

**Features:**
- Username field with validation rules
- Email field
- First and last name fields
- Role selector with descriptions
- Password fields (with strength requirements)
- Validation error display
- "Login" link for existing users
- Password requirements list

#### 3. Logout Confirmation (`accounts/logout_confirm.html`)
**Purpose:** Confirm logout action

**Features:**
- Logout confirmation message
- Confirm and cancel buttons

## Static Files Configuration

### Directory Structure
```
static/
└── css/
    └── style.css

media/
├── post_images/      # Featured images for posts
└── uploads/          # CKEditor uploaded content
```

### Media File Handling

**Settings Configuration:**
```python
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**URL Configuration:**
```python
# In development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**Post Image Uploads:**
- Path: `media/post_images/`
- Configured in Post model: `upload_to='post_images/'`
- Supports: JPG, PNG, GIF, WebP
- Displayed with responsive sizing

**CKEditor Uploads:**
- Path: `media/uploads/`
- Configured in settings: `CKEDITOR_UPLOAD_PATH = 'uploads/'`
- Embedded in post content
- Full rich text support

## Custom CSS Features

### Color Scheme
```css
--primary-color: #2c3e50;      /* Dark blue-gray */
--secondary-color: #3498db;     /* Bright blue */
--accent-color: #e74c3c;        /* Red */
--success-color: #27ae60;       /* Green */
--warning-color: #f39c12;       /* Orange */
```

### Component Styles

**Cards:**
- Border radius: 10px
- Hover effect: translateY(-5px) + enhanced shadow
- Smooth transitions

**Post Images:**
- Consistent heights (300px for list, 500px max for detail)
- Object-fit: cover for proper cropping
- Rounded corners (8px)

**Badges:**
- Role badges: Color-coded by user role
- Category/Tag badges: Clickable with hover effects
- Pill-shaped design (border-radius: 20px)

**Buttons:**
- Border radius: 6px
- Hover effect: translateY(-2px)
- Consistent padding and spacing

**Comments:**
- Threaded layout with left border
- Reply indentation: 2rem
- Hover effects on comment items

**Forms:**
- Enhanced focus states
- Consistent border radius (6px)
- Custom validation styling

### Responsive Design

**Breakpoints:**
- Mobile: < 768px
- Tablet: 768px - 991px
- Desktop: ≥ 992px

**Mobile Optimizations:**
- Disabled card hover animations
- Reduced comment reply indentation
- Smaller image heights (200px)
- Single column layouts
- Collapsible navigation

## Accessibility Features

1. **Semantic HTML:** Proper use of header, nav, main, article, footer tags
2. **ARIA Labels:** Added to navigation and interactive elements
3. **Alt Text:** Required for all images
4. **Keyboard Navigation:** All interactive elements are keyboard accessible
5. **Color Contrast:** WCAG AA compliant color combinations
6. **Focus Indicators:** Clear focus states on interactive elements

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance Optimizations

1. **CDN Usage:** Bootstrap and icons loaded from CDN
2. **Image Optimization:** Responsive images with proper sizing
3. **CSS Minification:** WhiteNoise for static file compression
4. **Lazy Loading:** Images below fold can be lazy-loaded
5. **Efficient Selectors:** Optimized CSS with minimal specificity

## Future Enhancements

1. **Dark Mode:** CSS variables ready for dark theme
2. **Progressive Web App:** Service worker integration
3. **Advanced Animations:** GSAP or Framer Motion
4. **Infinite Scroll:** Replace pagination on post lists
5. **Real-time Comments:** WebSocket integration
6. **Image Optimization:** Automatic thumbnail generation
7. **Syntax Highlighting:** Code blocks in posts
8. **Social Sharing:** Open Graph meta tags

## Usage Instructions

### Serving Static Files in Development
```bash
python manage.py collectstatic --noinput
```

### Creating Media Directories
```bash
mkdir -p media/post_images media/uploads
```

### Testing Responsive Design
1. Use browser DevTools responsive mode
2. Test on actual devices
3. Check all breakpoints (mobile, tablet, desktop)
4. Verify navigation collapse/expand
5. Test image scaling

### Custom CSS Modifications
1. Edit `/static/css/style.css`
2. Run `collectstatic` if in production mode
3. Clear browser cache
4. Refresh to see changes

## Template Inheritance Chain

```
base.html
├── blog/home.html
├── blog/post_list.html
├── blog/post_detail.html
├── blog/post_form.html
├── blog/my_posts.html
├── blog/draft_posts.html
├── blog/category_list.html
├── blog/category_detail.html
├── blog/tag_list.html
├── blog/tag_detail.html
├── blog/post_search.html
├── accounts/login.html
├── accounts/register.html
└── accounts/logout_confirm.html
```

## Important Notes

1. **Image Uploads:** Ensure the `media` directory has proper write permissions
2. **Static Files:** Run `collectstatic` before deploying to production
3. **CDN Fallback:** Consider local Bootstrap files for offline development
4. **CKEditor:** Requires internet connection for full functionality
5. **File Size Limits:** Configure max upload size in settings if needed

## Testing Checklist

- [ ] All templates extend base.html correctly
- [ ] Navigation works on all screen sizes
- [ ] Images display properly with fallbacks
- [ ] Forms validate and show errors
- [ ] Pagination works correctly
- [ ] Comments display and thread properly
- [ ] User roles show appropriate UI elements
- [ ] Static files load correctly
- [ ] Media uploads work
- [ ] Responsive design works on mobile
- [ ] All links and buttons function
- [ ] Error pages display nicely
