from django import template
import md5

register = template.Library()

@register.filter(is_safe=True)
def get_avatar(value, size=None):
	hash_value = md5.new(value.strip().lower()).hexdigest()
	return ('https://secure.gravatar.com/avatar/%s?d=retro' % hash_value) + (('&s=%s' % size) if size else '')
