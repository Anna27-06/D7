from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import Post
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Subscription
from django.conf import settings


@shared_task
def info_after_new_post(pk):
    new_post = Post.objects.get(pk=pk)
    categories = new_post.category.all()
    subscribers = []

    for category in categories:
        for user in category.get_sub():
            subscribers.append(user)

    subscribers = set(subscribers)

    for subscribe in subscribers:
        html_content = render_to_string(
            'new_post_notify.html',
            {
                'user': subscribe,
                'text': new_post.preview,
                'link': f'{settings.SITE_URL}{new_post.get_absolute_url()}'
            }
        )

        msg = EmailMultiAlternatives(
            subject=new_post.title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscribe.email],
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@shared_task
def weekly_send_email_task():
    today = timezone.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(post_time__gte=last_week).order_by('-post_time')
    category = set(posts.values_list('category__id', flat=True))
    subscribers_emails = set(
        Subscription.objects.filter(category__id__in=category).values_list('user__email', flat=True)
    )

    for subscriber_email in subscribers_emails:
        subscriptions_to_category = Subscription.objects.filter(user__email=subscriber_email)
        list_subscriptions_to_category = set(subscriptions_to_category.values_list('category', flat=True))
        subscribed_posts = posts.filter(postcategory__category__in=list_subscriptions_to_category).distinct()

        subject = 'Новости и статьи за прошедшую неделю по вашим подпискам'
        from_email = None
        to_email = subscriber_email

        text_content = render_to_string(
            'news_posts_email.txt',
            {'subscribed_posts': subscribed_posts, 'link': settings.SITE_URL}
        )
        html_content = render_to_string(
            'news_posts_email.html',
            {'subscribed_posts': subscribed_posts, 'link': settings.SITE_URL}
        )

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()