from django import template

register = template.Library()

@register.filter
def speed_format(value):
    formatting = 1024 * 1024
    value = '{0:.2f}'.format(value / formatting)
    return value + " " +"Mbit/s"

@register.filter
def ping_format(value):
    value = round(value)
    return value

@register.filter
def qos_format(value):
    value = '{0:.2f}'.format(value)
    return value + '' +  '%'