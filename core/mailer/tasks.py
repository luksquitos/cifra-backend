from django.utils.module_loading import import_string

from core.jobs import celery_app


@celery_app.task(name="send_email")
def send_email(email_template_path: str, **context):
    """
    :param str email_template_path: Attribute used in features.user.UserToken Model to load 
    specific template and send the email
    
    :param dict context: Context to initialize a EmailTemplate instance.
    
    Example:
    >>> Class UserConfirmEmailToken(UserToken):
            email_template_path = "features.user.emails.ConfirmationEmail"
    """
    email_template = import_string(email_template_path)
    email = email_template(**context)
    email.send()

    return {
        "message": "Email enviado",
        "email_template_path": email_template_path,
        "emails": context.get("to_emails"),
    }
