from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class Util:
    @staticmethod
    def send_email(data):
        from_email = 'Django App <{}>'.format(settings.EMAIL_HOST_USER)

        try:
            send_mail(
                subject=data["subject"],
                message=data["body"],
                recipient_list=[data["to_email"]],
                from_email=from_email,
                fail_silently=False,
            )
            logger.info(f"Email sent successfully to {data['to_email']}")

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise 
