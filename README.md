# 🦤 Dodos Code — Django Website

## Quick Start

```bash
# 1. Install Django
pip install django

# 2. Run migrations
python manage.py migrate

# 3. Create admin user
python manage.py createsuperuser

# 4. Start server
python manage.py runserver

# 5. Open browser
# Website: http://127.0.0.1:8000/
# Admin:   http://127.0.0.1:8000/admin/
```

## Admin Panel
- URL: `/admin/`
- Default: admin / admin123
- Add Services, Projects, Testimonials from admin

## Structure
```
dodos_code/
├── core/
│   ├── models.py      → Service, Project, ContactMessage, Testimonial
│   ├── views.py       → home view (handles contact form too)
│   ├── urls.py        → URL routing
│   ├── admin.py       → Admin registration
│   └── templates/core/home.html → Main website template
└── dodos_code/
    ├── settings.py
    └── urls.py
```

## Features
- ✅ Custom cursor with smooth ring animation
- ✅ Animated hero with stats counter
- ✅ Services grid with hover effects
- ✅ Projects showcase
- ✅ Contact form (saves to DB)
- ✅ Admin panel for content management
- ✅ Scroll reveal animations
- ✅ Fully responsive

## Customize
Edit `core/templates/core/home.html` for design changes.
Add content via Django Admin at `/admin/`
