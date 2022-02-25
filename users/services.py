from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def send_register_email(user):
    msg_html = render_to_string("users/email/registration.html", {"u": user})
    msg = EmailMessage(
        subject="SearchBot: Thanks for registering!",
        body=msg_html,
        from_email=settings.EMAIL_HOST_USER,
        bcc=[user.email],
    )
    msg.content_subtype = "html"
    msg.send()
