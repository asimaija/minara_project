from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """Split a string by the given delimiter."""
    return [item.strip() for item in str(value).split(arg) if item.strip()]
