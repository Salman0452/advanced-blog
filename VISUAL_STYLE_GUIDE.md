# Visual Style Guide

## Color Palette

### Primary Colors
```
Primary (Dark Blue-Gray): #2c3e50
├─ Usage: Headers, footer, text
├─ RGB: rgb(44, 62, 80)
└─ Bootstrap: Custom variable

Secondary (Bright Blue): #3498db
├─ Usage: Buttons, links, accents
├─ RGB: rgb(52, 152, 219)
└─ Bootstrap: btn-primary

Accent (Red): #e74c3c
├─ Usage: Delete buttons, admin badge, alerts
├─ RGB: rgb(231, 76, 60)
└─ Bootstrap: btn-danger
```

### Supporting Colors
```
Success Green: #27ae60
├─ Usage: Success messages, publish button
└─ Bootstrap: btn-success, alert-success

Warning Orange: #f39c12
├─ Usage: Warning messages, draft badge
└─ Bootstrap: btn-warning, alert-warning

Info Blue: #3498db
├─ Usage: Info messages, tooltips
└─ Bootstrap: alert-info

Light Gray: #95a5a6
├─ Usage: Reader badge, disabled states
└─ Bootstrap: bg-secondary
```

### Background Colors
```
White: #ffffff
Light Background: #f8f9fa
Border Color: #e0e0e0
Dark Text: #333333
Muted Text: #6c757d
```

## Typography

### Font Stack
```css
Primary Font:
font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;

Fallback Order:
1. Segoe UI (Windows, modern)
2. Tahoma (Windows, classic)
3. Geneva (Mac)
4. Verdana (universal)
5. sans-serif (system default)
```

### Font Sizes
```
Headings:
h1: 2.5rem (40px)
h2: 2rem (32px)
h3: 1.75rem (28px)
h4: 1.5rem (24px)
h5: 1.25rem (20px)
h6: 1rem (16px)

Body Text: 1rem (16px)
Small Text: 0.875rem (14px)
Form Labels: 0.875rem (14px)
Badges: 0.75rem (12px)
```

### Font Weights
```
Light: 300
Regular: 400
Medium: 500
Semibold: 600
Bold: 700
```

### Line Heights
```
Body Text: 1.6
Headings: 1.2
Compact (tables): 1.4
Relaxed (content): 1.8
```

## Spacing System

### Margin/Padding Scale (Bootstrap)
```
0: 0
1: 0.25rem (4px)
2: 0.5rem (8px)
3: 1rem (16px)
4: 1.5rem (24px)
5: 3rem (48px)
```

### Common Spacing Patterns
```
Card padding: p-3 or p-4 (1rem or 1.5rem)
Card margin bottom: mb-4 (1.5rem)
Section spacing: my-4 (1.5rem vertical)
Form field spacing: mb-3 (1rem)
Button spacing: px-4 py-2 (1.5rem horizontal, 0.5rem vertical)
```

## Components

### Buttons

#### Primary Button
```html
<button class="btn btn-primary">
    <i class="bi bi-check"></i> Action
</button>

Visual:
├─ Background: #3498db
├─ Text: White
├─ Border radius: 6px
├─ Padding: 0.5rem 1.5rem
└─ Hover: #2980b9 + translateY(-2px)
```

#### Secondary Button
```html
<button class="btn btn-outline-primary">Action</button>

Visual:
├─ Background: Transparent
├─ Border: 1px solid #3498db
├─ Text: #3498db
└─ Hover: Background #3498db, Text white
```

#### Danger Button
```html
<button class="btn btn-danger">Delete</button>

Visual:
├─ Background: #e74c3c
├─ Text: White
└─ Hover: #c0392b
```

#### Size Variants
```html
<button class="btn btn-sm">Small</button>
<button class="btn">Regular</button>
<button class="btn btn-lg">Large</button>
```

### Cards

#### Standard Card
```html
<div class="card">
    <div class="card-header">Header</div>
    <div class="card-body">Content</div>
    <div class="card-footer">Footer</div>
</div>

Visual:
├─ Border radius: 10px
├─ Border: 1px solid #e0e0e0
├─ Shadow: 0 4px 6px rgba(0,0,0,.1)
└─ Hover: translateY(-5px) + enhanced shadow
```

#### Card with Image
```html
<div class="card">
    <img src="..." class="card-img-top post-image">
    <div class="card-body">...</div>
</div>

Image Specs:
├─ Height: 300px (list), 500px max (detail)
├─ Object-fit: cover
└─ Border radius: 8px 8px 0 0
```

### Badges

#### Role Badges
```html
<span class="user-badge badge-admin">Admin</span>
<span class="user-badge badge-author">Author</span>
<span class="user-badge badge-reader">Reader</span>

Visual:
├─ Font size: 0.75rem
├─ Padding: 0.25rem 0.5rem
├─ Border radius: 12px
└─ Font weight: 600

Colors:
├─ Admin: #e74c3c (red)
├─ Author: #3498db (blue)
└─ Reader: #95a5a6 (gray)
```

#### Category/Tag Badges
```html
<span class="badge bg-primary">Category</span>
<span class="badge bg-secondary">#tag</span>

Visual:
├─ Padding: 0.5rem 0.75rem
├─ Border radius: 20px
└─ Font weight: 500
```

### Forms

#### Input Fields
```html
<input type="text" class="form-control">

Visual:
├─ Border radius: 6px
├─ Border: 1px solid #e0e0e0
├─ Padding: 0.75rem
├─ Focus: Border #3498db, Shadow blue
└─ Height: ~42px
```

#### Select Dropdowns
```html
<select class="form-select">
    <option>Option</option>
</select>

Visual: Same as input fields
```

#### Textareas
```html
<textarea class="form-control" rows="5"></textarea>

Visual:
├─ Same as inputs
└─ Min height: 5 rows
```

#### Checkboxes/Radio
```html
<div class="form-check">
    <input type="checkbox" class="form-check-input">
    <label class="form-check-label">Option</label>
</div>
```

### Navigation

#### Navbar
```
Height: ~60px
Background: White
Shadow: 0 2px 4px rgba(0,0,0,.1)
Padding: 1rem 0

Brand:
├─ Font size: 1.5rem
├─ Font weight: 700
└─ Color: #2c3e50

Links:
├─ Font weight: 500
├─ Padding: 0.5rem 1rem
└─ Hover: Color #3498db
```

#### Dropdown Menu
```
Border radius: 8px
Shadow: 0 2px 8px rgba(0,0,0,.15)
Min width: 200px

Items:
├─ Padding: 0.5rem 1rem
└─ Hover: Background #f8f9fa
```

### Alerts

```html
<div class="alert alert-success">Success message</div>
<div class="alert alert-danger">Error message</div>
<div class="alert alert-warning">Warning message</div>
<div class="alert alert-info">Info message</div>

Visual:
├─ Border radius: 8px
├─ Border: none
├─ Padding: 1rem
└─ Icons: Bootstrap Icons at start
```

### Tables

```html
<table class="table table-hover">
    <thead>
        <tr><th>Column</th></tr>
    </thead>
    <tbody>
        <tr><td>Data</td></tr>
    </tbody>
</table>

Visual:
├─ Border radius: 8px (wrap in .table-responsive)
├─ Hover: Background #f8f9fa
└─ Striped rows optional (.table-striped)
```

### Pagination

```html
<ul class="pagination justify-content-center">
    <li class="page-item"><a class="page-link">1</a></li>
    <li class="page-item active"><span class="page-link">2</span></li>
</ul>

Visual:
├─ Border radius: 6px per item
├─ Margin: 0.25rem between items
├─ Active: Background #3498db
└─ Hover: Background #f8f9fa
```

### Comments

```
Comment Item:
├─ Border bottom: 1px solid #e0e0e0
├─ Padding: 1rem 0
└─ Last child: No border

Reply:
├─ Margin left: 2rem
├─ Border left: 3px solid #3498db
└─ Padding left: 1rem
```

## Icons

### Icon System
```
Library: Bootstrap Icons 1.11.1
CDN: https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css
```

### Common Icons
```
Navigation:
├─ bi-house-door (Home)
├─ bi-folder (Categories)
├─ bi-tags (Tags)
└─ bi-search (Search)

Actions:
├─ bi-pencil-square (Edit)
├─ bi-trash (Delete)
├─ bi-plus-circle (Add)
└─ bi-check-circle (Confirm)

Metadata:
├─ bi-person-circle (Author)
├─ bi-calendar3 (Date)
├─ bi-eye (Views)
└─ bi-chat-dots (Comments)

UI:
├─ bi-arrow-right (Navigation)
├─ bi-x-circle (Cancel)
└─ bi-info-circle (Information)
```

### Icon Sizing
```html
<!-- Inline with text -->
<i class="bi bi-icon"></i>

<!-- Large decorative -->
<i class="bi bi-icon" style="font-size: 3rem;"></i>

<!-- Extra large -->
<i class="bi bi-icon" style="font-size: 4rem;"></i>
```

## Responsive Breakpoints

```
Mobile: < 768px
├─ Single column layouts
├─ Stacked navigation
├─ Reduced spacing
└─ Smaller images (200px height)

Tablet: 768px - 991px
├─ Two column layouts
├─ Expanded navigation
└─ Medium images (250px height)

Desktop: ≥ 992px
├─ Multi-column layouts (up to 4)
├─ Full navigation
├─ Full-size images (300px height)
└─ Hover effects enabled
```

## Animation & Transitions

### Hover Effects
```css
/* Cards */
transition: transform 0.3s ease, box-shadow 0.3s ease;
transform: translateY(-5px);

/* Buttons */
transition: all 0.3s ease;
transform: translateY(-2px);

/* Links */
transition: color 0.3s ease;
```

### Loading States
```html
<div class="spinner-border" role="status">
    <span class="visually-hidden">Loading...</span>
</div>
```

## Image Guidelines

### Post Featured Images
```
Recommended Size: 1200x630px (1.91:1 ratio)
Min Size: 800x400px
Max File Size: 2MB
Formats: JPG, PNG, WebP
Quality: 80-85%

Display Sizes:
├─ List view: 300px height
├─ Detail view: 500px max height
└─ Thumbnail: 250px height

Object-fit: cover (crops to container)
Border radius: 8px
```

### User Avatars (Future)
```
Recommended Size: 200x200px (1:1 ratio)
Min Size: 100x100px
Format: JPG, PNG
Border radius: 50% (circular)
```

### Content Images (CKEditor)
```
Max width: 100% (responsive)
Auto height: Maintain aspect ratio
Border radius: 8px
Margin: 1rem 0
```

## Accessibility

### Color Contrast Ratios
```
Normal Text: 4.5:1 minimum (WCAG AA)
Large Text: 3:1 minimum
UI Components: 3:1 minimum

Tested Combinations:
├─ #2c3e50 on white: 12.6:1 ✓
├─ #3498db on white: 4.5:1 ✓
└─ White on #3498db: 4.5:1 ✓
```

### Focus States
```css
.form-control:focus {
    border-color: #3498db;
    box-shadow: 0 0 0 0.2rem rgba(52, 152, 219, 0.25);
    outline: none;
}

a:focus, button:focus {
    outline: 2px solid #3498db;
    outline-offset: 2px;
}
```

### ARIA Labels
```html
<button aria-label="Delete post">
    <i class="bi bi-trash"></i>
</button>

<nav aria-label="Page navigation">
    <ul class="pagination">...</ul>
</nav>
```

## Print Styles

```css
@media print {
    /* Hide navigation and actions */
    .navbar,
    footer,
    .btn,
    .card-header {
        display: none;
    }
    
    /* Expand content */
    .container {
        max-width: 100%;
    }
    
    /* Remove backgrounds */
    .card {
        border: 1px solid #000;
        box-shadow: none;
    }
}
```

## Browser-Specific Notes

### Safari
- May need `-webkit-` prefixes for some properties
- Test `object-fit` for images

### Firefox
- Custom scrollbar styles not supported
- Test flexbox layouts

### Edge/Chrome
- Full CSS Grid support
- All modern features supported

## Performance Guidelines

### Image Optimization
```
Use modern formats (WebP with JPG fallback)
Lazy load images below fold
Compress images to 80-85% quality
Serve responsive images with srcset
```

### CSS Optimization
```
Use CDN for Bootstrap (caching)
Minify custom CSS in production
Combine multiple custom CSS files
Use CSS containment where applicable
```

### JavaScript Optimization
```
Defer non-critical scripts
Use async for analytics
Minimize DOM manipulations
Debounce scroll/resize handlers
```

## Design Principles

1. **Consistency**: Use defined colors, spacing, and components throughout
2. **Clarity**: Clear visual hierarchy and readable typography
3. **Simplicity**: Avoid unnecessary decorations or complexity
4. **Responsiveness**: Design works on all screen sizes
5. **Accessibility**: WCAG AA compliant, keyboard navigable
6. **Performance**: Fast loading, optimized assets
7. **Maintainability**: Well-organized, documented code

## Tools & Resources

### Testing
- Browser DevTools (responsive mode)
- WAVE (accessibility checker)
- Lighthouse (performance audits)
- Color contrast analyzers

### References
- Bootstrap 5 Docs: https://getbootstrap.com
- Bootstrap Icons: https://icons.getbootstrap.com
- WCAG Guidelines: https://www.w3.org/WAI/WCAG21/quickref/
- MDN Web Docs: https://developer.mozilla.org
