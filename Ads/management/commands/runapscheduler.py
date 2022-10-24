import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
import datetime

from Ads.models import Ad


logger = logging.getLogger(__name__)


def my_job():
    """Set the time interval during which ads is collected from the server and
    get all ads"""
    time_now = (datetime.datetime.utcnow() - datetime.timedelta(days=7))
    ads = Ad.objects.filter(date_creation__gte=time_now)
    """Get all user which we send email and the emails of the receivers"""
    users = User.objects.all()
    emails_receivers = []
    for user in users:
        if user.email:
            emails_receivers.append(user.email)
    """Forming and sending email"""
    html_content = render_to_string(
        'Ads/mail_message7day.html',

        {
            'ads': ads,
        },
        )
    send_mail(
        subject='Новые новости на нашем портале за последнюю неделю',
        message=html_content,
        from_email='seleznevaiu86@mail.ru',
        recipient_list=emails_receivers,
        fail_silently=False,
        html_message=html_content,
            )


def delete_old_job_executions(max_age=604860):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(week="01"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                week="01", second="05"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

