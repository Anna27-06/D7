from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import PostCategory
from .tasks import info_after_new_post


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        info_after_new_post.delay(instance.pk)



# def product_created(sender, instance, action, **kwargs):
#     if action == 'post_add':
#         emails = User.objects.filter(
#             subscriptions__category__in=instance.category.all()
#         ).values_list('email', flat=True)
#
#         subject = f'Новый пост в категории {instance.category.all()}'
#
#         text_content = (
#             f'Пост: {instance.title}\n'
#             f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
#         )
#         html_content = (
#             f'Пост: {instance.title}<br>'
#             f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
#             f'Ссылка на пост</a>'
#         )
#         for email in emails:
#             msg = EmailMultiAlternatives(subject, text_content, None, [email])
#             msg.attach_alternative(html_content, "text/html")
#             msg.send()