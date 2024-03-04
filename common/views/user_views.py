from django.contrib.auth import authenticate, login,logout, update_session_auth_hash
from django.shortcuts import render,redirect
from django.contrib import messages
from common.forms import UserForm,ModifyForm
from django.db.models import Count
from common.media_form import UserProfile, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from diary.forms import CreateDiary, Answer
from django.core.paginator import Paginator  
from django.contrib.auth.forms import PasswordChangeForm
import os
from django.conf import settings


def logout_view(request):
    logout(request)
    return redirect('diary:index')

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # User 모델 저장
            messages.success(request, '회원가입이 완료되었습니다')

            # 프로필 이미지 업로드
            profile_image = request.FILES.get('profile_image')
            if profile_image:
                user_profile = UserProfile.objects.create(user=user, profile_image=profile_image)

            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

@login_required(login_url='common:login')
def update(request):
    if request.method == 'POST' :
        form = ModifyForm(request.POST, instance=request.user)
        if form.is_valid() :
            form.save()
            messages.success(request, '회원정보가 성공적으로 변경되었습니다.')
            return redirect('common:mypage')
    else :
        form = ModifyForm(instance=request.user)

    return render(request, 'common/update.html', {'form': form})

@login_required(login_url='common:login')
def modify_password(request):
    if request.method == 'POST' :
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid() :
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, '비밀번호가 성공적으로 변경되었습니다.')
            return redirect('common:mypage')
    else :
        form = PasswordChangeForm(request.user)

    return render(request, 'common/modify_password.html', {'form': form})

@login_required(login_url='login')
def delete(request) :
    if request.user.is_authenticated :
        request.user.delete()
        logout(request)
        messages.success(request, '회원탈퇴가 완료되었습니다. 그동안 감사했습니다.')
        return redirect('index')
    


@login_required(login_url='common:login')
def mypage(request):
    current_user_id = request.user.id # 현재 로그인 한사람 

    page = request.GET.get('page','1') # 페이지

    # 현재 로그인된 사용자가 적은 일기중 public 된것만 가져오기
    diary_list1 = CreateDiary.objects.filter(author_id=current_user_id).order_by('-create_date')

    # 현재 로그인된 사용자가 작성한 댓글이 있는 CreateDiary 가져오기
    user_comment_diary = Answer.objects.filter(author_id=current_user_id).values('question_id').annotate(question_count=Count('question_id')).order_by('-question_count')
    comment_diary = [CreateDiary.objects.get(pk=question['question_id']) for question in user_comment_diary]

    # 현재 로그인한 사용자가 추천한(public) 일기 중 voter(추천)를 누른 CreateDiary 가져오기
    user_recommend_diary = CreateDiary.objects.filter(disclose='public', voter__id=current_user_id)

    # 현재 로그인한 사용자가 작성한(public) 글 중 voter(추천)를 받은 CreateDiary 가져오기
    recommend_diary = CreateDiary.objects.filter(author_id=current_user_id, voter__isnull=False)

    user_profile = UserProfile.objects.filter(user=request.user).first()  # 프로필 조회
    if user_profile:
        image_path = user_profile.profile_image.url if user_profile.profile_image else None
    else:
        image_path = None

    # Paginator 적용
    paginator_diary_list1 = Paginator(diary_list1, 5)
    paginator_comment_diary = Paginator(comment_diary, 5)
    paginator_user_recommend_diary = Paginator(user_recommend_diary, 5)
    paginator_recommend_diary = Paginator(recommend_diary, 5)

    page_diary_list1 = paginator_diary_list1.get_page(page)
    page_comment_diary = paginator_comment_diary.get_page(page)
    page_user_recommend_diary = paginator_user_recommend_diary.get_page(page)
    page_recommend_diary = paginator_recommend_diary.get_page(page)

    context = {
        'user_profile': user_profile,
        'image_path': image_path,
        'page_diary_list1': page_diary_list1,
        'page_comment_diary': page_comment_diary,
        'page_user_recommend_diary': page_user_recommend_diary,
        'page_recommend_diary': page_recommend_diary,
    }
    return render(request, 'common/my_page.html', context)

def profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        image_path = user_profile.profile_image.url if user_profile.profile_image else None
    except UserProfile.DoesNotExist:
        # 사용자 프로필이 없는 경우, 새로운 프로필을 생성합니다.
        user_profile = UserProfile.objects.create(user=request.user)
        image_path = None

    context = {'user_profile': user_profile, 'image_path': image_path}
    return render(request, 'common/profile.html', context)

def profile_update(request):
    if request.method == "POST":
        # 현재 사용자의 프로필을 가져옴 / 만약 프로필이 없는 경우 빈 프로필을 생성
        user_profile,created = UserProfile.objects.get_or_create(user=request.user)

        # 기존 파일이 존재하는지 확인하고 삭제
        previous_image_path = user_profile.profile_image.path if user_profile.profile_image else None
        if previous_image_path:
            if os.path.exists(previous_image_path):
                os.remove(previous_image_path)

        form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():

            form.save() # 폼 데이터 저장
            return redirect('common:mypage') # 프로필 업데이트 후에는 마이 페이지로 이동
    else:
        # GET 요청일 때는 현재 사용자의 프로필을 가져와 폼에 넘겨줌
        user_profile,created = UserProfile.objects.get_or_create(user=request.user)
        form = ProfileUpdateForm(instance=user_profile)
    
    return render(request, 'common/profile_update.html', {'form': form})


