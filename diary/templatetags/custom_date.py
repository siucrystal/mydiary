from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()

@register.filter
def relative_time(date):
    
    now = timezone.now()
    date_diff = now - date

    if date_diff < timedelta(minutes=1):
        return '방금 전'
    elif date_diff < timedelta(hours=1):
        return str(int(date_diff.seconds / 60)) + '분 전'
    elif date_diff < timedelta(days=1):
        return str(int(date_diff.seconds / 3600)) + '시간 전'
    elif date_diff < timedelta(days=2):
        return '어제'
    elif date_diff < timedelta(days=7):
        return str(int((date_diff.days))+1 ) + '일 전'
    else:
        if date.year == now.year:
            return date.strftime('%m월 %d일')
        else:
            return date.strftime('%Y년 %m월 %d일')