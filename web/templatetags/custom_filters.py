from django import template

register = template.Library()


@register.filter
def team_logo_path(team_key):
    return f"/static/img/MLB/{team_key}.png"


@register.filter
def remove_leading_zero(value):
    if isinstance(value, float):
        return f'{value:.3f}'.lstrip(0)
    return value
