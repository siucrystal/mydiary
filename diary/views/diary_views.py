from django.shortcuts import render, get_object_or_404, redirect
from ..models import CreateDiary
from django.utils import timezone
from ..models import CreateDiary
from ..forms import DiaryForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url='common:login')
def diary_create(request):
    if request.method == 'POST':
        form = DiaryForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = form.cleaned_data['create_date']
            question.photo = request.FILES.get('photo')
            question.save()
            return redirect('diary:index')
    else:
        form = DiaryForm()

    
    context = {'form': form}
    return render(request, 'diary/diary_form.html', context)


@login_required(login_url='common:login')
def diary_modify(request, diary_id):
    diary = get_object_or_404(CreateDiary, pk=diary_id)
    if request.user != diary.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('diary:detail', diary_id=diary.diary_id)
    if request.method == "POST":
        form = DiaryForm(request.POST, request.FILES, instance=diary)
        if form.is_valid():
            diary = form.save(commit=False)
            diary.modify_date = timezone.now()  # 수정일시 저장
            if 'img_delete' in request.POST:
                diary.photo.delete()  # 이미지 삭제
            diary.save()
            return redirect('diary:detail', diary_id=diary.diary_id)
    else:
        form = DiaryForm(instance=diary)
    context = {'form': form}
    return render(request, 'diary/diary_modify.html', context)


@login_required(login_url='common:login')
def diary_delete(request, diary_id):
    diary = get_object_or_404(CreateDiary, pk=diary_id)
    if request.user != diary.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('diary:detail', diary_id=diary.diary_id)
    diary.delete()
    return redirect('diary:index')

