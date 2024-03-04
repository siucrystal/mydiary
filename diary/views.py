from django.shortcuts import render, get_object_or_404, redirect
from .models import CreateDiary
from django.utils import timezone

def index(request):
    diary_list = CreateDiary.objects.order_by('-create_date')
    context = {'diary_list':diary_list}
    return render(request, 'diary/diary_list.html', context)

def detail(request, diary_id):
    diary = CreateDiary.objects.get(diary_id=diary_id)
    context = {'diary':diary}
    return render(request, 'diary/diary_detail.html', context)

def answer_create(request, diary_id):
    question = get_object_or_404(CreateDiary, pk=diary_id)
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    return redirect('diary:detail', diary_id=diary_id)
