from celery import shared_task
from pythonthaibulksms.django import django_thaibulksms_sms


@shared_task
def django_thaibulksms_sms_celery(
        msisdn,
        message,
        config='default',
        schedule=None
    ):
        django_thaibulksms_sms(
            msisdn,
            message,
            config=config,
            schedule=schedule
        )