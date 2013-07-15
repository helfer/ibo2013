from django.template import Library

register = Library()
print "run"
@register.filter
def is_false(arg): 
    return arg is False


