from django.shortcuts import render, get_object_or_404, redirect
from ..models import CreateDiary, Answer
from django.utils import timezone
from ..models import CreateDiary
from ..forms import DiaryForm, AnswerForm
from django.core.paginator import Paginator  
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count


@login_required(login_url='common:login')
def answer_create(request, diary_id):
    diary = get_object_or_404(CreateDiary, pk=diary_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = diary
            answer.save()
            return redirect('diary:detail', diary_id=diary.diary_id)
    else:
        form = AnswerForm()
    context = {'diary': diary, 'form': form}
    return render(request, 'diary/diary_detail.html', context)

@login_required(login_url='common:login')
def answer_modify(request, answer_id, diary_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    diary = get_object_or_404(CreateDiary, pk=diary_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('diary:detail', diary_id=diary.diary_id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('diary:detail', diary_id=diary.diary_id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'diary/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id, diary_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    diary = get_object_or_404(CreateDiary, pk=diary_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('diary:detail', diary_id=diary.diary_id)


