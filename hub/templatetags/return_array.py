from django import template

register = template.Library()


@register.filter
def return_array(l, i):
    try:
        return l[i]
    except:
        return None

