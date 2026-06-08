from django.db import models

class Service(models.Model):
    icon = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.IntegerField(default=0)
    class Meta:
        ordering = ['order']
    def __str__(self):
        return self.title

class Project(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    description = models.TextField()
    tech_stack = models.CharField(max_length=200)
    color = models.CharField(max_length=20, default='cyan')
    store_link = models.URLField(blank=True, null=True, help_text="App Store / Play Store / Live URL")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    service = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} - {self.email}"

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    message = models.TextField()
    rating = models.IntegerField(default=5)
    def __str__(self):
        return self.name
