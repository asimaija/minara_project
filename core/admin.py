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
    fields = ['title', 'category', 'description', 'tech_stack', 'color', 'store_link', 'thumbnail']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'service', 'created_at']
    readonly_fields = ['created_at']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'rating']
