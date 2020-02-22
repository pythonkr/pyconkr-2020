from django.shortcuts import render

# Create your views here.
from pyconkr.models import Announcement


def index(request):
    return render(request, 'web2020/index.html', {
        'index': True,
        # 'base_content': FlatPage.objects.get(url='/index/').content,
        'recent_announcements': Announcement.objects.all()[:3],
    })