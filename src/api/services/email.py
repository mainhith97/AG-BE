import threading

from django.conf import settings
from django.core.mail import EmailMessage


class EmailThread(threading.Thread):
    def __init__(self, subject=None, content=None, email=None):
        self.subject = subject
        self.content = content
        self.sender = settings.EMAIL_HOST_USER
        self.recipient_list = email
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(subject=self.subject, body=self.content, from_email=self.sender,
                           to=self.recipient_list, cc=None, bcc=None)
        msg.content_subtype = 'html'
        msg.send()
