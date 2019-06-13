from django import template

# Custom template tags

register = template.Library()

@register.simple_tag
def slice_list(option, the_list):
    if option == 1:
        return the_list[:4]
    elif option == 2:
        return the_list[4:8]