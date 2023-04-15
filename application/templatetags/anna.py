from django import template
from django.db.models import Count, Q

from application.models import Module

register = template.Library()


@register.simple_tag
def previous_module_completed(module, user):
    qs = (
        Module.data.filter(next=module.id)
        .annotate(
            completed_count=Count("media__completed", filter=Q(media__completed__user=user))
        )
        .order_by("ordering")
    )
    if qs.exists():
        if qs.first().progress <= 99:
            return False
    return True
