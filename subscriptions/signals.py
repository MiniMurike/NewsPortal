from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from AllNews.models import PostCategory, CATEGORY_CATEGORIES
from .models import Subscription


@receiver(m2m_changed, sender=PostCategory)
def post_created(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        post_categories_qs = instance.post_category.all()

        categories = ''
        subscribers = []

        for category in post_categories_qs:

            subscribers += (list(
                Subscription.objects.filter(
                    category=category
                ).values_list('user__email', flat=True)))

            categories = f'{category} {categories}'

        subject = f'Новая запись в категории {categories}'

        text_content = (
            f'Заголовок: {instance.title}\n'
            f'Содержание: {instance.text[:15]}...\n\n'
            f'Подробнее...->: http://localhost:8000{instance.get_absolute_url()}{instance.pk}'
        )

        html_content = (
            f'Заголовок: {instance.title}<br>'
            f'Содержание: {instance.text[:15]}...<br><br>'
            f'<a href="http://localhost:8000{instance.get_absolute_url()}{instance.pk}">'
            f'Подробнее...-></a>'
        )

        # Чистка повторений пользователей, если те указали несколько категорий для рассылки
        subscribers = list(set(subscribers))

        for email in subscribers:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
