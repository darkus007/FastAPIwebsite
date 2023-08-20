"""
Модуль содержит конфигурацию и точку входа Celery
для выполнения фоновых задач по отправке e-mail,
функцию по отправке e-mail.


Запуск Celery:
celery -A src.tasks.celery_tasks:celery worker --loglevel=INFO

Запуск Flower:
celery -A src.tasks.celery_tasks:celery flower
"""

import smtplib

from celery import Celery

from src.config import settings
from src.tasks.email_maker import EmailMaker

celery = Celery('tasks', broker=settings.redis_url)


@celery.task
def send_email(user_email: str, token: str, content: str | None = None):
    """
    Отправляет сообщение пользователю.

    :param user_email: e-mail пользователя, которому будет отправлено сообщение;
    :param token: токен для аутентификации пользователя;
    :param content: определяет тип сообщения (по умолчанию верификация e-mail)
    """

    if content == "forgot_password":
        email = EmailMaker.forgot_password(user_email, token)
    else:
        email = EmailMaker.email_verify(user_email, token)

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        if not settings.SMTP_DEBUG:  # если не используем отладочный SMTP, то логинимся
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(email)
