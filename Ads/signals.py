from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Response


@receiver(post_save, sender=Response)
def notify_new_post(sender, instance, created, **kwargs):
    receiver_email = None
    if created:
        subject = 'Новый отклик на объявление'
        receiver_email = instance.ad.author.email
        user_response = instance.user
        ad = instance.ad
        answer_to_ad = instance.text_response
        html_content = render_to_string(
            'Ads/mail_message_response.html',
            {
                'ad': ad,
                'user_response': user_response,
                'answer_to_ad': answer_to_ad,
            },
        )
        send_mail(
            subject=subject,
            message=html_content,
            from_email='seleznevaiu86@mail.ru',
            recipient_list=[receiver_email],
            fail_silently=False,
            html_message=html_content,
            )

    else:
        if instance.accepted:
            receiver_email = instance.user.email
            subject = 'Ваш отклик на объявление принят'
            author_ad = instance.ad.author
            ad = instance.ad
            html_content = render_to_string(
                'Ads/mail_message_accept_response.html',
                {
                    'ad': ad,
                    'author_ad': author_ad,
                },
            )
            send_mail(
                subject=subject,
                message=html_content,
                from_email='seleznevaiu86@mail.ru',
                recipient_list=[receiver_email],
                fail_silently=False,
                html_message=html_content,
            )
