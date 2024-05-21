from django import template
import datetime

from django.db.models import Count
from mainapp.models import Category
from mainapp.utils import menu


register = template.Library()


@register.simple_tag
def get_menu():
    return menu


@register.simple_tag(name='current_time')
def current_time(format:str = None):
    if format is not None:
        return "Текущее время: " + str(datetime.datetime.now().strftime(format))
    else:
        return "Текущее время: " + str(datetime.datetime.now())


@register.inclusion_tag('women/list_categories.html')
def show_categories():
    cats = Category.objects.annotate(total=Count('posts')).filter(total__gt=0)
    return {'cats': cats,}