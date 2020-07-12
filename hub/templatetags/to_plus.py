from django import template

register = template.Library()


@register.filter
def to_plus(value):
    value = value.split(" x ")[1] if " x " in value else value
    return value.replace(" ", "+")

