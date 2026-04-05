# from django import template
# register = template.Library()

# @register.filter
# def get_item(lst, id):
#     for item in lst:
#         if item.id == int(id):
#             return item
#     return None

# @register.filter
# def dict_get(dictionary, key):
#     return dictionary.get(int(key))

# @register.filter
# def multiply(value, arg):
#     try:
#         return float(value) * float(arg)
#     except (ValueError, TypeError):
#         return 0
    
from django import template
register = template.Library()

@register.filter
def get_item(lst, id):
    try:
        for item in lst:
            if item.id == int(id):
                return item
    except (ValueError, TypeError, AttributeError):
        return None
    return None

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0