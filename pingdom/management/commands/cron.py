import datetime
import urllib2

from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from pingdom.models import UserProfile


class Command(BaseCommand):
    @staticmethod
    def handle(*args, **options):
        INBOX_MESSAGE_INV_NOTIFICATION_BODY_TMPL = 'email_templates/url_mail_error.html'
        user = UserProfile.objects.all()
        for site in user:
            from_user = site.user.email
            to_user = site.user.email
            site_user = site.hassites.all()
            for url in site_user:
                if url.auto_test_mode:
                    try:
                        urllib2.urlopen(url.url)
                        url.date = datetime.datetime.now()
                        url.testsuc += 1
                        url.save()
                    except urllib2.HTTPError, error:
                        url.date = datetime.datetime.now()
                        url.testfail += 1
                        url.save()
                        subject = "Please Check this Url Is Down This Time"
                        body = 'Error', error
                        inbox_body = render_to_string(INBOX_MESSAGE_INV_NOTIFICATION_BODY_TMPL,
                                                      {'site_user': site.user.email, 'Subject': subject, 'error': error,
                                                       'url': url.url})
                        emailmsg = EmailMultiAlternatives(subject, inbox_body, from_user, [to_user])
                        emailmsg.attach_alternative(inbox_body, "text/html")
                        emailmsg.send()
                        url.date = datetime.datetime.now()
                        url.mailsent += 1
                        url.save()
                    except urllib2.URLError, error:
                        url.date = datetime.datetime.now()
                        url.testfail += 1
                        url.save()
                        subject = 'Network unreachable'
                        body = 'Error', error
                        inbox_body = render_to_string(INBOX_MESSAGE_INV_NOTIFICATION_BODY_TMPL,
                                                      {'site_user': site.user.email, 'Subject': subject, 'error': error,
                                                       'url': url.url})
                        emailmsg = EmailMultiAlternatives(subject, inbox_body, from_user, [to_user])
                        emailmsg.attach_alternative(inbox_body, "text/html")
                        emailmsg.send()
                        url.date = datetime.datetime.now()
                        url.mailsent += 1
                        url.save()
