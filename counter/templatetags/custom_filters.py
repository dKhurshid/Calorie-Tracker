from django import template

register = template.Library()

@register.filter
def div(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return None

@register.filter
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return None

@register.filter
def default_if_none(value, default):
    return value if value is not None else default


@register.filter
def subtract(value, arg):
    return value - arg