from django import template

# Custom template filters

register = template.Library()

@register.filter
def modify(num):
    mag = 0
    while num >= 1000.0:
        mag += 1
        num /= 1000.0
    
    return (str(int(num)) + ['', 'K', 'M', 'B', 'T',][mag] + ('+' if (num - int(num) > 0.0) else ''))
