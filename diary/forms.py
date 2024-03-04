from django import forms
from diary.models import CreateDiary, Answer


class DiaryForm(forms.ModelForm):
    class Meta:
        model = CreateDiary  # 사용할 모델
        fields = ['weather', 'mood', 'title', 'content', 'photo', 'reflection', 'praise', 'disclose', 'create_date', 'modify_date']  # QuestionForm에서 사용할 Question 모델의 속성
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']  # create_date 필드 제외
        labels = {
            'content': '답변내용',
        }