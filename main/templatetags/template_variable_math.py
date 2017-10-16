from django import template

register = template.Library()

@register.filter
def template_variable_sum(value1, value2):
	return int(value1) - int(value2)