from django.shortcuts import render, get_object_or_404, redirect
from ..models import CreateDiary, Answer
from django.utils import timezone
from ..forms import DiaryForm, AnswerForm
from django.core.paginator import Paginator  
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.db.models import Q 
from django import template
from ..templatetags.custom_date import relative_time
from common.views import mypage
from common.media_form import UserProfile
from datetime import date
from django.http import JsonResponse
from django.forms.models import model_to_dict
from datetime import timedelta

register = template.Library()
register.filter('relative_time', relative_time)

def index(request):
    return render(request, 'index.html')

def diary_list(request):
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')
    
    if year and month and day:
        try:
            day = int(day)
            # day 값에서 1을 빼기
            day += 1
            create_date = date(int(year), int(month), day)
        except ValueError:
            create_date = None
    else :
        create_date = None

    if create_date:
        diary_list = CreateDiary.objects.filter(
            author_id=request.user.id,
            create_date=create_date
        ).order_by('-create_date')
    else:
        diary_list = CreateDiary.objects.filter(author_id=request.user.id).order_by('-create_date')

    paginator = Paginator(diary_list, 10) # 페이지당 10개씩 보여주기
    page = request.GET.get('page','1') # 페이지
    page_obj = paginator.get_page(page)

    context = {'diary_list':page_obj}

    return render(request, 'diary/diary_list.html', context)

def diary_ajax(request):
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')
    
    if year and month and day:
        try:
            create_date = date(int(year), int(month), int(day) )
        except ValueError:
            create_date = None
    else :
        create_date = None

    if create_date:
        diary_list = CreateDiary.objects.filter(
            author_id=request.user.id,
            create_date=create_date
        ).order_by('-create_date')
    else:
        diary_list = CreateDiary.objects.filter(author_id=request.user.id).order_by('-create_date')

    data = []
    for diary in diary_list:
        print('diary : ', diary)
        diary_dict = model_to_dict(diary)
        # 필요한 필드만 선택하여 딕셔너리에 추가
        diary_data = {
            'create_date': diary_dict['create_date'],
            'title': diary_dict['title'],
            'disclose': diary_dict['disclose'],
            # 필요한 필드 추가
        }
        data.append(diary_data)
    return JsonResponse(data, safe=False)


def detail(request, diary_id):
    diary = CreateDiary.objects.get(diary_id=diary_id)
    create_date = diary.create_date
    previous_day = create_date - timedelta(days=1)

    try:
        user_profile = UserProfile.objects.get(user_id=diary.author_id)
        if user_profile :
            image_path = user_profile.profile_image.url if user_profile.profile_image else None
        else:
            image_path = None
    except UserProfile.DoesNotExist:
        image_path = None

    context = {'diary':diary, 'image_path':image_path, 'previous_day': previous_day}
    return render(request, 'diary/diary_detail.html', context)


@login_required(login_url='common:login')
def diary_vote(request, diary_id):
    diary = get_object_or_404(CreateDiary, pk=diary_id)
    if request.user == diary.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        diary.voter.add(request.user)
    return redirect('diary:detail', diary_id=diary.diary_id)

def diary_every(request):
    page = request.GET.get('page','1') # 페이지
    diary_list2 = CreateDiary.objects.filter(disclose='public').order_by('-create_date')
    
    # Best Diaries comment
    most_common_questions = Answer.objects.values('question_id').annotate(question_count=Count('question_id')).order_by('-question_count')[:3]
    best_diaries = [CreateDiary.objects.get(pk=question['question_id']) for question in most_common_questions]
    
    # Best Diaries recommend
    recommend_questions = CreateDiary.objects.annotate(voter_count=Count('voter')).order_by('-voter_count')[:3]

    # 검색 
    
    content = request.GET.get('content','전체')
    kw = request.GET.get('kw', '')  # 검색어

    if content == '전체':
        diary_list2 = diary_list2
    elif content == '제목/내용':
        diary_list2 = diary_list2.filter(
            Q(title__icontains=kw)  # 제목 검색
        ).distinct()
    elif content == '답변':
        diary_list2 = diary_list2.filter(
            Q(content__icontains=kw)  # 내용 검색
        ).distinct()
    elif content == '일기 글쓴이':
        diary_list2 = diary_list2.filter(
            Q(author__username__icontains=kw)  # 질문 글쓴이 검색
        ).distinct()
    elif content == '답변 글쓴이':
        diary_list2 = diary_list2.filter(
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    else :
        diary_list2 = diary_list2.filter(
            Q(title__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    # kw = request.GET.get('kw', '')  # 검색어
    # if kw:
    #     diary_list2 = diary_list2.filter(
    #         Q(title__icontains=kw) |  # 제목 검색
    #         Q(content__icontains=kw) |  # 내용 검색
    #         Q(answer__content__icontains=kw) |  # 답변 내용 검색
    #         Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
    #         Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
    #     ).distinct()


    paginator = Paginator(diary_list2, 10) # 페이지당 10개씩 보여주기                                                   
    page_obj = paginator.get_page(page)

    context = {
        'diary_list2':page_obj,
        'best_diaries': best_diaries,
        'recommend_questions': recommend_questions,
        'page': page, 'kw': kw
    }

    return render(request, 'diary/diary_every_list.html', context)