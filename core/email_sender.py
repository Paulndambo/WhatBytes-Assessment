from datetime import date

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils.html import strip_tags


class SendMessage(object):
    def __init__(self):
        """
        This class is used to send messages, it can have a method for sending an email, an sms or other types of messages

        Note: I didn't provide any thing here since i wanted to handle different types of messages
        like sms, emails, slack message etc, which will surely have different parameters.
        """
        pass

    def send_mail(self, context_data, recipient_list, template=None):
        try:
            from_email = settings.SITE_EMAIL
            context_data["email_date"] = str(date.today())

            if template:
                html_message = get_template(
                    "messages/{0}.html".format(template)
                ).render(context_data)
            else:
                html_message = get_template("messages/send_message.html").render(
                    context_data
                )

            message = strip_tags(html_message)

            subject = "{0}- {1}".format(settings.EMAIL_SUBJECT, context_data["subject"])

            headers = {
                "Reply-To": settings.SITE_EMAIL,
                "From": settings.SITE_EMAIL,
            }

            email = EmailMultiAlternatives(
                subject=subject,
                body=message,
                from_email=from_email,
                to=recipient_list,
                headers=headers,
            )
            email.attach_alternative(html_message, "text/html")

            if "attached_files" in context_data:
                for attached_file in context_data["attached_files"]:
                    email.attach(
                        attached_file["name"],
                        attached_file["main_file"],
                        attached_file["media_type"],
                    )
            email.send()
        except Exception as e:
            print(f"_send_email >> error in sending email > {e}")
            raise e

    def send_sms(self, name, phone_number):
        """Incase there is a need to send sms to users, logic can be configured here"""
        pass
