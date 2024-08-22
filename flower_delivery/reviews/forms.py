from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.HiddenInput(),  # Мы используем скрытое поле для рейтинга, т.к. управление идет через JavaScript
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'rating': 'Рейтинг',
            'comment': 'Ваш отзыв',
        }


