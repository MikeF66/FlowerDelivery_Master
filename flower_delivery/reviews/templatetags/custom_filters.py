from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def star_rating(rating):
   if rating is None or rating == '':
       rating = 0  # Если рейтинг отсутствует, используем значение по умолчанию 0
   full_stars = int(rating)
   half_star = 1 if rating % 1 >= 0.5 else 0
   empty_stars = 5 - full_stars - half_star

   stars = '<i class="fas fa-star"></i>' * full_stars
   if half_star:
       stars += '<i class="fas fa-star-half-alt"></i>'
   stars += '<i class="far fa-star"></i>' * empty_stars

   return mark_safe(stars)


@register.filter
def pluralize_reviews(count):
    try:
        count = abs(int(count))  # Преобразуем значение в целое число
    except (ValueError, TypeError):
        return 'отзывов'  # В случае ошибки вернем форму "отзывов" по умолчанию

    if count % 10 == 1 and count % 100 != 11:
        return 'отзыв'
    elif count % 10 in [2, 3, 4] and count % 100 not in [12, 13, 14]:
        return 'отзыва'
    else:
        return 'отзывов'


@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})

