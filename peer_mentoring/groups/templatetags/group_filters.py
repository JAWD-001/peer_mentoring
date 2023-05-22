from django import template

register = template.Library()


@register.filter
def can_join(group, user):
    return group.can_join(user)
