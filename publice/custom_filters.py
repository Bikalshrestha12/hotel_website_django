from django import template

register = template.Library()

@register.filter
def length_is(value, arg):
    """Returns True if the length of value equals the argument"""
    try:
        return len(value) == int(arg)
    except (TypeError, ValueError):
        return False