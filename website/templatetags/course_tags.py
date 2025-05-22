from django import template

register = template.Library()

@register.filter
def is_selected(selected, current):
    return selected == current