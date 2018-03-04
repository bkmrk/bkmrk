from flask import render_template, current_app

from bkmrk.email import send_email


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    admin_email = current_app.config['MAIL_ADMIN'][0] if current_app.config['MAIL_ADMIN'] else None
    send_email('[BKMRK] Reset Your Password',
        sender=admin_email,
        recipients=[user.email],
        text_body=render_template('email/reset_password.txt', user=user, token=token),
        html_body=render_template('email/reset_password.html', user=user, token=token))
