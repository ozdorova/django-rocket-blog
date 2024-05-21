from django import template


register = template.Library()


@register.filter
def make_title(string):
    return string.title()