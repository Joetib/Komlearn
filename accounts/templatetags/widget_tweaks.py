from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.filter
def add_class(form_widget, css_class):
	""" Adds a css class to a django form widget """
	return form_widget.as_widget(attrs={'class': css_class})



@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
