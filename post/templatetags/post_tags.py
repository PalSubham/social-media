from django import template

# Custom template tags

register = template.Library()

@register.simple_tag
def slice_list(beg, end, the_list):
    return the_list[int(beg):int(end)]