import click

from app import db
from app.models import User


def register(app):
    """ Command in cmd """
    @app.cli.command('createsuperuser')
    @click.argument('data')
    def createsuperuser(data):
        """ Create super user (USERNAME_PASSWORD_EMAIL) """
        username, password, email = data.split('_')
        user = User(username=username, email=email)
        user.set_password(password)
        user.permission = 'admin'
        db.session.add(user)
        db.session.commit()
