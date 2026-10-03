# Blogify

Blogify is a Django blogging website that I built as a learning project
while learning Django and working with authentication, content
management, roles and permissions, and databases.

The project has a public blogging side where users can browse and read
posts, and a dashboard where authorized users can manage posts,
categories, users, and comments.

## Live Demo

<https://shibithp94.pythonanywhere.com/>

## GitHub Repository

<https://github.com/shibith-dev/blogify-complete-blogging-system>

## Features

### Public Blog

-   Home page with featured articles and recent posts
-   Browse posts by category
-   View all published posts
-   View featured posts
-   Search posts by title, description, content, category, or author
-   Sort posts by latest or oldest
-   Pagination for post lists
-   Individual blog post pages
-   Related posts
-   Comments on blog posts
-   About section and social links
-   Newsletter subscription UI

### Authentication

-   User registration
-   Login and logout
-   Django's built-in authentication system
-   Password validation using Django's built-in validators

### Dashboard

The dashboard is available to logged-in users and provides different
access depending on the user's role and Django permissions.

-   Dashboard overview with post, category, comment, and user counts
-   Create, edit, and delete blog posts
-   Upload featured images for posts
-   Set a post as Draft or Published
-   Mark posts as Featured
-   Create, edit, and delete categories
-   View and manage users
-   Assign groups and permissions to users
-   View and delete comments
-   Search and filter dashboard data
-   Pagination for dashboard lists

### User Roles

The project uses Django Groups and permissions for role-based access.

The main roles used in the project are:

-   **Manager** - can manage the wider blog content and users based on
    assigned permissions
-   **Editor** - can manage blog content and other permitted areas
-   **Author** - can manage their own blog posts and related content
    based on permissions
-   **Superuser** - has the highest level of access through Django's
    admin and the dashboard

Authors are restricted to their own posts in the dashboard, while
Managers and Editors can work with posts across the site when they have
the required permissions.

## Technologies Used

-   Python
-   Django 5.2.17
-   SQLite
-   HTML
-   CSS
-   Bootstrap 4
-   django-crispy-forms
-   crispy-bootstrap4
-   Pillow
-   python-dotenv

## Project Structure

``` text
blogify-complete-blogging-system/
│
├── base/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   └── admin.py
│
├── blogs/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── context_processors.py
│   └── admin.py
│
├── dashboards/
│   ├── migrations/
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── blogify_main/
│   ├── static/
│   ├── forms.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
│   ├── dashboard/
│   ├── home.html
│   ├── posts.html
│   ├── blog.html
│   ├── login.html
│   └── register.html
│
├── media/
├── manage.py
├── requirements.txt
└── .gitignore
```

## Main Django Apps

### `base`

Contains the basic site information used by the blog, such as the About
section and social links.

### `blogs`

This is the main blogging app. It contains the models and views for:

-   Categories
-   Blog posts
-   Comments
-   Searching
-   Category filtering
-   Featured posts
-   Post details

### `dashboards`

Contains the logged-in dashboard and the content management
functionality.

It handles post management, category management, user management,
comments, and role/permission-based access.

## Database Models

The main models in the project are:

-   `Category` - stores blog categories
-   `Blog` - stores blog posts, authors, categories, images,
    descriptions, content, status, and featured state
-   `Comment` - stores comments made by authenticated users
-   `About` - stores the About section shown on the website
-   `SocialLink` - stores social media links

Django's built-in `User`, `Group`, and permission system is used for
authentication and role management.

## Getting Started

### 1. Clone the repository

``` bash
git clone https://github.com/shibith-dev/blogify-complete-blogging-system.git
cd blogify-complete-blogging-system
```

### 2. Create a virtual environment

On Windows:

``` bash
python -m venv venv
venv\Scripts\activate
```

On macOS/Linux:

``` bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the dependencies

``` bash
pip install -r requirements.txt
```

### 4. Create the environment file

The project reads the Django secret key from an environment variable.

Create a `.env` file in the project root:

``` env
SECRET_KEY=your-secret-key-here
```

For a local development project, you can generate a new Django secret
key instead of using a key from another environment.

Do not commit your `.env` file to GitHub.

### 5. Apply migrations

``` bash
python manage.py migrate
```

### 6. Create a superuser

``` bash
python manage.py createsuperuser
```

Follow the prompts to create the admin account.

### 7. Run the development server

``` bash
python manage.py runserver
```

Then open:

``` text
http://127.0.0.1:8000/
```

## Setting Up User Roles

Blogify uses Django Groups for roles such as `Manager`, `Editor`, and
`Author`.

After creating a superuser, you can use the Django admin panel to create
the required groups and assign permissions to users.

Open:

``` text
http://127.0.0.1:8000/admin/
```

The dashboard checks the user's group membership and Django permissions
before allowing access to different management actions.

## Creating a Blog Post

A logged-in user with the required permission can create a post from the
dashboard.

A post contains:

-   Title
-   Category
-   Featured image
-   Short description
-   Blog body
-   Status
-   Featured option

The status can be either `Draft` or `Published`.

When a post is created, its slug is generated from the title and post
ID.

## Django Admin

The project also uses Django's built-in admin panel.

The admin panel can be used to manage:

-   Categories
-   Blog posts
-   Comments
-   Users
-   Groups
-   Permissions

The blog admin also provides search and filtering options for posts.

## Screenshots

The project has a public blog interface and a separate dashboard
interface.

The main screens include:

-   Home page
-   All Posts page
-   Blog post detail page
-   Dashboard
-   Dashboard post management
-   Add Post
-   Edit Post

Screenshots of these pages are included with the project showcase and
can also be added to a `docs/screenshots/` folder if the repository is
being used as a portfolio project.

## Deployment

The project is deployed and currently available on PythonAnywhere.

Live website:

<https://shibithp94.pythonanywhere.com/>

The local development configuration uses SQLite. Deployment settings can
be configured separately depending on the hosting environment.

## What I Learned

This project helped me practice several parts of Django instead of only
building a basic CRUD application.

Some of the main things I worked with are:

-   Django project and app structure
-   Models and database relationships
-   Django ORM queries
-   Forms and ModelForms
-   Authentication
-   Django Groups and permissions
-   Login-required views
-   Permission-protected views
-   File and image uploads
-   Templates and template inheritance
-   Static and media files
-   Pagination
-   Search and filtering
-   Django admin
-   Environment variables
-   Basic deployment with PythonAnywhere

## Future Improvements

Some things I would like to improve in the future:

-   Add a richer editor for writing blog posts
-   Add email verification and password reset
-   Add more automated tests
-   Improve deployment and production settings
-   Add more features for post engagement, such as likes, comment reply or bookmarks,

## Note

This project was built mainly as a learning and portfolio project to
understand how the different parts of a Django application work
together. It is not intended to be presented as a production-ready
blogging platform.

## Author

Built by **Shibith**.

GitHub: <https://github.com/shibith-dev>
