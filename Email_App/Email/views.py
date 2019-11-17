from django.shortcuts import render
from django.core.mail import EmailMessage
# To work on mail connection
from django.core import mail
# Importing settings to populate from_email field
from django.conf import settings
# Importing our customized form
from . forms import SendEmail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
# Timestamp for email
from django.utils import timezone
from . models import EmailStats

import logging
logger = logging.getLogger(__name__)


def send_email(request):

    logger.info('Email Triggered.')

    if request.method == 'POST':
        logger.info('POST Method')
        form = SendEmail(request.POST)
        result = ''
        if form.is_valid():

            # Manually opening the connection
            connection = mail.get_connection()
            connection.open()
            logger.info('Connection Opened')

            # Extracting the data entered by the user in the form
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            from_email = settings.EMAIL_HOST_USER
            recipient_list = form.cleaned_data['to']
            cc_list = form.cleaned_data['cc']
            bcc_list = form.cleaned_data['bcc']

            # If the To field is populated via CSV File
            if not recipient_list:
                logger.info("No recipients in To field.")

                logger.info("CSV File detected.")
                csv_file = request.FILES["csv_file"]

                logger.info("Reading CSV File.")
                file_data = csv_file.read().decode("utf-8")

                emails = []

                import csv
                import io
                io_string = io.StringIO(file_data)

                for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                    # Validating the emails in CSV file
                    try:
                        validate_email(column[0])
                        valid_email = True
                    except ValidationError:
                        valid_email = False
                        result = 'The CSV file contains Invalid email address: ', column[0]
                        logger.error('The CSV file contains Invalid email address: ', column[0])
                    if valid_email:
                        emails.append(column[0])

                # print('Emails:', emails)

                recipient_list = emails

            logger.info('Email Fields:', subject, body, from_email, recipient_list, cc_list, bcc_list)

            # Creating an EmailMessage Object
            email = EmailMessage(subject=subject, body=body, from_email=from_email,
                                 to=recipient_list, bcc=bcc_list, cc=cc_list)

            # Calling the send function
            email.send(fail_silently=False)
            timestamp = timezone.now()

            # Closing the connection
            connection.close()
            logger.info('Connection closed.')
            logger.info('Successfully sent the email.')

            email_log = EmailStats(subject=subject, timestamp=timestamp)
            email_log.save()

            return render(request, 'Email/Successful.html', {'result': result})
        else:
            result = 'Form validation failed.'
            logger.error('Form validation failed.')
            return render(request, 'Email/Failed.html', {'result': result})

    else:
        logger.info('Loading the form.')
        form = SendEmail()

    return render(request, 'Email/Send_Email.html', {'form': form})

