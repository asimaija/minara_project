from django.contrib import admin
from .models import Service, Project, ContactMessage, Testimonial

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'order']
    ordering = ['order']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'store_link', 'created_at']
    list_editable = ['store_link']
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'category', 'description'),
        }),
        ('Tech & Links', {
            'fields': ('tech_stack', 'color', 'store_link', 'thumbnail'),
            'description': (
                '⚠️ tech_stack: comma-separated e.g.  Django, React, PostgreSQL  — '
                'thumbnail is optional (emoji icon shown if blank)'
            ),
        }),
    )

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'service', 'created_at']
    readonly_fields = ['created_at']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'rating']