from flask import render_template, current_app

from app.send_mail import send_email


def send_admin_about_order(order):
    """ Send admins about the order """
    send_email('Flask ecommerce, New order', sender=current_app.config['ADMINS'][0],
               recipients=current_app.config['ADMINS'],
               text_body=render_template('email/new_order.txt', order=order),
               html_body=render_template('email/new_order.html', order=order))
