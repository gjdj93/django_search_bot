from .models import Search
from bs4 import BeautifulSoup
import urllib.request
from urllib.error import HTTPError
from django.utils import timezone
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def find_items():
    searches = Search.objects.all()

    for s in searches:
        if not s.found:
            try:
                page = urllib.request.urlopen(s.url)
                soup = BeautifulSoup(page, features="html.parser")
                if s.phrase.lower() in soup.text.lower():
                    print(f"{s.phrase} found on {s.url}")
                else:
                    print(f"{s.phrase} not found on {s.url}")
                    s.found = True
                    s.date_found = timezone.now()
                    s.save()
                    msg_html = render_to_string("searches/email/found.html", {"s": s})
                    msg = EmailMessage(
                        subject="SearchBot: Your product is now available!",
                        body=msg_html,
                        from_email=settings.EMAIL_HOST_USER,
                        bcc=[s.user.email],
                    )
                    msg.content_subtype = "html"
                    msg.send()

            except HTTPError as e:
                if e.code == 403:
                    print("Website forbidden")
                else:
                    print("Error parsing website")
