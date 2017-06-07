from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.simple_tag()
def define(the_string):
    return the_string


somevariable = []
@register.simple_tag
def define_variable(variable):
    global somevariable
    somevariable = variable
    return somevariable



@register.simple_tag
def get_var():
    global somevariable
    return somevariable