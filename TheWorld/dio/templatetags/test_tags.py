from django import template

register = template.Library()


@register.simple_tag(name='multi_decimal')
def multi_decimal(v1, v2):
    value1 = float(v1)
    value2 = float(v2)
    rst = "%.2f" %(value1*value2)
    return rst
