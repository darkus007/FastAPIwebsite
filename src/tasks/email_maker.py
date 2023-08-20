"""
Модуль содержит логику создания e-mail сообщений.

Базовый класс EmailTemplate, который в качестве аргументов принимает:
    user_email - e-mail пользователя, которому будет отправлено сообщение;
    token - токен для аутентификации пользователя;
    content_maker - вызываемый объект, который возвращает html для помещения в тело письма.
Метод render возвращает экземпляр класса EmailMessage.

Фабрика EmailMaker, которая создает письма:
    email_verify - для верификации e-mail пользователя;
    forgot_password - для восстановления пароля пользователя.
"""

from abc import ABC, abstractmethod
from email.message import EmailMessage

from src.config import settings


class AbstractContentMaker(ABC):
    """
    Предоставляет html сообщение тела письма.
    """
    @abstractmethod
    def __call__(self,  user_email: str, token: str | None) -> str:
        ...


class EmailTemplate:
    def __init__(self, user_email: str, token: str | None, content_maker: AbstractContentMaker):
        """
        Рендерит e-mail шаблон.

        :param user_email: e-mail пользователя, которому будет отправлено сообщение;
        :param token: токен для аутентификации пользователя;
        :param content_maker: вызываемый объект (функция или класс),
        который возвращает html для помещения в тело письма.
        """
        self.user_email: str = user_email
        self.token: str = token
        self.content_maker: AbstractContentMaker = content_maker

    def render(self) -> EmailMessage:
        """
        Выполняет рендер e-mail шаблона.

        :return: EmailMessage.
        """
        email = EmailMessage()
        email['Subject'] = 'Подтверждение адреса E-mail'
        email['From'] = settings.SMTP_USER
        email['To'] = self.user_email
        email.set_content(self.content_maker(self.user_email, self.token),
                          subtype='html')
        return email


class VerifyContent(AbstractContentMaker):
    """
    Предоставляет html сообщение для валидации почты.
    """
    def __call__(self, user_email: str, token: str) -> str:
        content = '<div>' \
            '<h1>Здравствуйте,</h1>' \
            '<p>Благодарим за регистрацию на сайте по подбору жилья! Мы хотим убедиться, что вы являетесь владельцем ' \
            f'адреса электронной почты {user_email}. Пожалуйста, нажмите на ссылку ниже, чтобы подтвердить свой аккаунт:' \
            f'{token}</p>' \
            '<p>Подтвержденные пользователи могут использовать дополнительный функционал сайта - подписываться на отслеживание' \
            ' изменений по квартирам и получать оповещения на почту.</p>' \
            '<br>' \
            '<p>Если вы не регистрировались на нашем сайте, пожалуйста, проигнорируйте это сообщение.</p>' \
            '<br>' \
            '<p>С уважением, ' \
            'Администрация сайте по подбору жилья.</p>' \
            '</div>'
        return content


class ForgotPasswordContent(AbstractContentMaker):
    """
    Предоставляет html сообщение для восстановления пароля.
    """
    def __call__(self, user_email: str, token: str) -> str:
        content = '<div>' \
            '<h1>Здравствуйте,</h1>' \
            '<p>Вы получили это письмо, потому что запросили восстановление пароля на сайте по подбору жилья. ' \
            'Чтобы создать новый пароль, перейдите по ссылке ниже:' \
            f'{token}</p>' \
            '<br>' \
            '<p>Если вы не запрашивали восстановление пароля, проигнорируйте это сообщение.</p>' \
            '<br>' \
            '<p>С уважением, ' \
            'Администрация сайте по подбору жилья.</p>' \
            '</div>'
        return content


class EmailMaker:
    """
    Интерфейс для взаимодействия с данным модулем.
    """
    @staticmethod
    def email_verify(user_email: str, token: str) -> EmailMessage:
        return EmailTemplate(user_email, token, VerifyContent()).render()

    @staticmethod
    def forgot_password(user_email: str, token: str) -> EmailMessage:
        return EmailTemplate(user_email, token, ForgotPasswordContent()).render()
