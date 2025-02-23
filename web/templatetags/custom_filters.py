from django import template

register = template.Library()


@register.filter
def team_logo_path(team_key):
    return f"/static/img/MLB/{team_key}.png"
