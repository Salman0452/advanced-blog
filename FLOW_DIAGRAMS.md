# Authentication & Authorization Flow Diagram

## User Registration Flow
```
┌─────────────────────────────────────────────────────────────┐
│                    User Registration Flow                    │
└─────────────────────────────────────────────────────────────┘

User visits /accounts/register/
         ↓
    Is authenticated? ────YES───→ Redirect to home
         ↓ NO
    Display registration form
    (username, email, role, password)
         ↓
    User submits form
         ↓
    Validate input ────INVALID───→ Show errors
         ↓ VALID
    Create user account
    with selected role
         ↓
    Success message
         ↓
    Redirect to login page
```

## User Login Flow
```
┌─────────────────────────────────────────────────────────────┐
│                      User Login Flow                         │
└─────────────────────────────────────────────────────────────┘

User visits /accounts/login/
         ↓
    Is authenticated? ────YES───→ Redirect to home
         ↓ NO
    Display login form
    (username, password, remember_me)
         ↓
    User submits credentials
         ↓
    Authenticate user ────FAIL───→ Show error message
         ↓ SUCCESS
    Login user & create session
         ↓
    Set session expiry:
    - Remember Me: 2 weeks
    - Default: Browser close
         ↓
    Success message
         ↓
    Redirect to next URL or home
```

## Permission Check Flow
```
┌─────────────────────────────────────────────────────────────┐
│                   Permission Check Flow                      │
└─────────────────────────────────────────────────────────────┘

User attempts to access protected view
         ↓
    Is authenticated? ────NO────→ Redirect to login
         ↓ YES                    with "next" parameter
    Check role requirement
         ↓
    ┌────────────────────────────────────────┐
    │  RoleRequiredMixin (Base)              │
    │  - Checks if user.role in allowed_roles│
    └────────────────────────────────────────┘
         ↓
    ┌─────────────────┬─────────────────┬────────────────┐
    ↓                 ↓                 ↓                ↓
┌────────┐      ┌────────┐      ┌────────┐      ┌────────┐
│ Admin  │      │ Author │      │ Reader │      │ Owner  │
│Required│      │Required│      │Required│      │Required│
└────────┘      └────────┘      └────────┘      └────────┘
    ↓                 ↓                 ↓                ↓
Only Admin      Admin +          All auth'd       Check if
               Author           users          owner or Admin
         ↓
    Permission granted? ────NO────→ Show error message
         ↓ YES                      Redirect to home
    Grant access to view
```

## Role Hierarchy
```
┌─────────────────────────────────────────────────────────────┐
│                      Role Hierarchy                          │
└─────────────────────────────────────────────────────────────┘

                    ┌───────────────┐
                    │     ADMIN     │ (Full Access)
                    │ ───────────── │
                    │ • Manage all  │
                    │ • Moderate    │
                    │ • User mgmt   │
                    └───────┬───────┘
                            │
            ┌───────────────┴───────────────┐
            ↓                               ↓
    ┌───────────────┐              ┌───────────────┐
    │    AUTHOR     │              │    READER     │
    │ ───────────── │              │ ───────────── │
    │ • Create posts│              │ • Read posts  │
    │ • Edit own    │              │ • Add comments│
    │ • Comment     │              │ • Edit own    │
    └───────────────┘              └───────────────┘

                    ↓
            All inherit from
        ┌───────────────────────┐
        │    Authenticated      │
        │         User          │
        └───────────────────────┘
```

## Mixin Usage Examples
```
┌─────────────────────────────────────────────────────────────┐
│                    Mixin Usage Patterns                      │
└─────────────────────────────────────────────────────────────┘

VIEW TYPE                    MIXIN TO USE
─────────────────────────────────────────────────────────────
Public (anyone)              No mixin needed
─────────────────────────────────────────────────────────────
Create comment               ReaderRequiredMixin
Edit own comment             CommentOwnerRequiredMixin
─────────────────────────────────────────────────────────────
Create post                  AuthorRequiredMixin
Edit own post                AuthorOwnerRequiredMixin
Author dashboard             AuthorRequiredMixin
─────────────────────────────────────────────────────────────
Moderate comments            AdminRequiredMixin
Manage all posts             AdminRequiredMixin
User management              AdminRequiredMixin
─────────────────────────────────────────────────────────────
```

## Session Management
```
┌─────────────────────────────────────────────────────────────┐
│                   Session Management                         │
└─────────────────────────────────────────────────────────────┘

User logs in
     ↓
Remember Me checked?
     │
     ├──YES──→ Session expires: 2 weeks (1,209,600 seconds)
     │         User stays logged in across browser restarts
     │
     └──NO───→ Session expires: When browser closes
               User must login again after closing browser

Logout:
     ↓
User visits /accounts/logout/
     ↓
Confirmation page displayed
     ↓
User confirms logout
     ↓
Session destroyed
     ↓
Redirect to home with goodbye message
```

## Template Structure
```
┌─────────────────────────────────────────────────────────────┐
│                    Template Hierarchy                        │
└─────────────────────────────────────────────────────────────┘

                    base.html
                    │
                    ├── Navbar
                    │   ├── Logo/Brand
                    │   ├── Navigation Links
                    │   └── User Menu
                    │       ├── If authenticated:
                    │       │   ├── Username with role badge
                    │       │   ├── Profile
                    │       │   ├── My Posts (Author/Admin)
                    │       │   ├── Create Post (Author/Admin)
                    │       │   ├── Admin Panel (Admin)
                    │       │   └── Logout
                    │       └── If not authenticated:
                    │           ├── Login
                    │           └── Register
                    │
                    ├── Messages Section
                    │   ├── Success messages (green)
                    │   ├── Error messages (red)
                    │   ├── Warning messages (yellow)
                    │   └── Info messages (blue)
                    │
                    ├── Main Content Block
                    │   │
                    │   ├── accounts/register.html
                    │   │   └── Registration form
                    │   │
                    │   ├── accounts/login.html
                    │   │   └── Login form
                    │   │
                    │   ├── accounts/logout_confirm.html
                    │   │   └── Logout confirmation
                    │   │
                    │   └── blog/home.html
                    │       ├── Welcome section
                    │       ├── User dashboard (if auth'd)
                    │       ├── Posts list
                    │       └── Sidebar
                    │           ├── Permissions card
                    │           ├── Features card
                    │           └── Roles info card
                    │
                    └── Footer
                        ├── Brand info
                        └── Copyright
```

## Database Schema
```
┌─────────────────────────────────────────────────────────────┐
│                     Database Schema                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────┐
│   accounts_user     │ (Custom User Model)
├─────────────────────┤
│ id (PK)             │
│ username (unique)   │
│ email               │
│ password (hashed)   │
│ first_name          │
│ last_name           │
│ role ◄───────────── │ (Admin/Author/Reader)
│ bio                 │
│ profile_picture     │
│ is_staff            │
│ is_superuser        │
│ date_joined         │
└─────────┬───────────┘
          │
          │ 1:N (author)
          ↓
┌─────────────────────┐
│     blog_post       │
├─────────────────────┤
│ id (PK)             │
│ title               │
│ slug (unique)       │
│ content             │
│ excerpt             │
│ author_id (FK) ─────┤──→ points to accounts_user
│ category_id (FK)    │
│ status              │
│ featured_image      │
│ views_count         │
│ created_at          │
│ published_at        │
└─────────┬───────────┘
          │
          │ 1:N (post)
          ↓
┌─────────────────────┐
│   blog_comment      │
├─────────────────────┤
│ id (PK)             │
│ post_id (FK) ───────┤──→ points to blog_post
│ author_id (FK) ─────┤──→ points to accounts_user
│ parent_id (FK)      │──→ self-reference for replies
│ content             │
│ is_approved         │
│ created_at          │
└─────────────────────┘
```

## Access Control Summary
```
┌─────────────────────────────────────────────────────────────┐
│              Access Control Decision Tree                    │
└─────────────────────────────────────────────────────────────┘

Request to protected view
         ↓
    ┌─────────────┐
    │Authenticated?│─NO──→ Redirect to /accounts/login/
    └─────┬───────┘
          │YES
          ↓
    ┌──────────────┐
    │  Check Role  │
    └──────┬───────┘
           │
           ├──→ AdminRequiredMixin ──→ user.role == 'Admin'?
           │                           ├─YES──→ ALLOW
           │                           └─NO───→ DENY
           │
           ├──→ AuthorRequiredMixin ─→ user.role in ['Admin', 'Author']?
           │                           ├─YES──→ ALLOW
           │                           └─NO───→ DENY
           │
           ├──→ AuthorOwnerRequiredMixin ─→ Is Author/Admin?
           │                                 ├─YES──→ Is owner?
           │                                 │        ├─YES──→ ALLOW
           │                                 │        └─NO───→ Is Admin?
           │                                 │                ├─YES→ALLOW
           │                                 │                └─NO─→DENY
           │                                 └─NO───→ DENY
           │
           └──→ ReaderRequiredMixin ──→ Is authenticated?
                                        ├─YES──→ ALLOW
                                        └─NO───→ DENY
```
