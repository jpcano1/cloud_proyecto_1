from flask_mail import Message, Mail
from flask import current_app

mail = Mail()

def send_email(to, subject, template):
    """
    Function to send an email message
    :param to: The email destination
    :param subject: The email subject
    :param template: The HTML template to
    render the email
    """
    msg = Message(
        subject=subject,
        recipients=[to],
        html=template,
        sender=current_app.config["MAIL_DEFAULT_SENDER"]
    )
    mail.send(msg)