from django.urls import path
from django.contrib import admin
# 이미지를 업로드하자
from django.conf.urls.static import static
from django.conf import settings

from .views import base_views, diary_views, answer_views

app_name = 'diary'

urlpatterns = [
    path('', base_views.index, name='index'),
    path('diary/', base_views.diary_list, name='diary_list'),
    path('diary_ajax/', base_views.diary_ajax, name='diary_ajax'),
    path('diary/every', base_views.diary_every, name='diary_every'),
    path('diary/<int:diary_id>/', base_views.detail, name='detail'),
    path('answer/create/<int:diary_id>/', answer_views.answer_create, name='answer_create'),
    path('diary/create/', diary_views.diary_create, name='diary_create'),
    path('diary/modify/<int:diary_id>/', diary_views.diary_modify, name='diary_modify'),
    # path('diary/delete_photo/<int:diary_id>/', diary_views.delete_photo, name='delete_photo'),
    path('diary/delete/<int:diary_id>/', diary_views.diary_delete, name='diary_delete'),
    path('answer/modify/<int:answer_id>/<int:diary_id>/', answer_views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/<int:diary_id>/', answer_views.answer_delete, name='answer_delete'),
    path('diary/vote/<int:diary_id>/', base_views.diary_vote, name='diary_vote'),
]

# 이미지 URL 설정
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)