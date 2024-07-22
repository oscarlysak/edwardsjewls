from django import template
from home.models import Announcement

register = template.Library()

@register.simple_tag
def get_announcement_text():
    announcement = Announcement.objects.first()
    return announcement.text if announcement else "No announcements at this time."
