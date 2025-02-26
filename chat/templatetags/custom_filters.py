# templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, '')


@register.filter
def get_file_name(url):
    """Extracts the file name from a URL."""
    return url.split('/')[-1]