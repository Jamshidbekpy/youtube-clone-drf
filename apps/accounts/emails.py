from django.core.mail import EmailMessage

def send_custom_email(subject, message, recipient_email, user):
    if not hasattr(user, "userprofile") or not user.userprofile.smtp_host:
        return False  # SMTP ma'lumotlari yo'q bo'lsa, jo'natmaymiz

    email = EmailMessage(
        subject,
        message,
        user.userprofile.smtp_email,
        [recipient_email]
    )
    email.host = user.userprofile.smtp_host
    email.port = user.userprofile.smtp_port
    email.username = user.userprofile.smtp_email
    email.password = user.userprofile.smtp_password
    email.use_tls = True

    return email.send()
