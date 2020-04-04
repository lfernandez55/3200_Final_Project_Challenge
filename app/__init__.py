# __init__.py is a special Python file that allows a directory to become
# a Python package so it can be accessed using the 'import' statement.

from datetime import datetime
import os

from flask import Flask, url_for, Markup
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate, MigrateCommand
from flask_user import UserManager
from flask_wtf.csrf import CSRFProtect


# Instantiate Flask extensions
csrf_protect = CSRFProtect()
db = SQLAlchemy()
mail = Mail()
migrate = Migrate()

# Initialize Flask Application
def create_app(extra_config_settings={}):
    """Create a Flask application.
    """
    # Instantiate Flask
    app = Flask(__name__)

    # Load common settings
    app.config.from_object('app.settings')
    # Load environment specific settings
    app.config.from_object('app.local_settings')
    # Load extra settings from extra_config_settings param
    app.config.update(extra_config_settings)
    # Note config settings can be accessed like in following line:
    # print("MAIL_SERVER SETTING:",app.config['MAIL_SERVER'])
    # Setup Flask-SQLAlchemy
    db.init_app(app)

    # Setup Flask-Migrate
    migrate.init_app(app, db)

    # Setup Flask-Mail
    mail.init_app(app)

    # Setup WTForms CSRFProtect
    csrf_protect.init_app(app)

    # Register blueprints
    from .views import register_blueprints
    register_blueprints(app)

    # Define bootstrap_is_hidden_field for flask-bootstrap's bootstrap_wtf.html
    from wtforms.fields import HiddenField

    def is_hidden_field_filter(field):
        return isinstance(field, HiddenField)

    app.jinja_env.globals['bootstrap_is_hidden_field'] = is_hidden_field_filter

    # Setup an error-logger to send emails to app.config.ADMINS
    init_email_error_handler(app)

    # Setup Flask-User to handle user account related forms
    from .models.user_models import User
    from .views.main_views import user_profile_page

    # Setup Flask-User
    user_manager = UserManager(app, db, User)

    @app.context_processor
    def context_processor():
        return dict(user_manager=user_manager)

    # for more on context processors see (search on "context"): 
    # https://junxiandoc.readthedocs.io/en/latest/docs/flask/flask_template.html
    @app.context_processor
    def utility_processor():
        # renders the view if any of the passed in permitted_roles are in the current_user's roles
        def render(view,permitted_roles,linkname, current_user):
            # sqlStatement = "SELECT roles.name FROM roles JOIN users_roles ON roles.id=users_roles.role_id JOIN users ON users.id=users_roles.user_id WHERE users.email='" + current_user.email + "' AND roles.name='admin'"
            sqlStatement = "SELECT roles.name FROM roles JOIN users_roles ON roles.id=users_roles.role_id JOIN users ON users.id=users_roles.user_id WHERE users.email='" + current_user.email + "'"
            roleName = db.engine.execute(sqlStatement)
            # Casting the returned alchemy query object into a list
            # See https://stackoverflow.com/questions/1958219/convert-sqlalchemy-row-object-to-python-dict
            roleName = [dict(row) for row in roleName]
            display_link = False
            for user_role in roleName:
                 if user_role['name'] in permitted_roles:
                    display_link = True
            if display_link:
                link = "<a  href='" + url_for(view) + "'>" + linkname + "</a>"
                return Markup(link)
        return dict(render=render)

    return app


def init_email_error_handler(app):
    """
    Initialize a logger to send emails on error-level messages.
    Unhandled exceptions will now send an email message to app.config.ADMINS.
    """
    if app.debug: return  # Do not send error emails while developing

    # Retrieve email settings from app.config
    host = app.config['MAIL_SERVER']
    port = app.config['MAIL_PORT']
    from_addr = app.config['MAIL_DEFAULT_SENDER']
    username = app.config['MAIL_USERNAME']
    password = app.config['MAIL_PASSWORD']
    secure = () if app.config.get('MAIL_USE_TLS') else None

    # Retrieve app settings from app.config
    to_addr_list = app.config['ADMINS']
    subject = app.config.get('APP_SYSTEM_ERROR_SUBJECT_LINE', 'System Error')

    # Setup an SMTP mail handler for error-level messages
    import logging
    from logging.handlers import SMTPHandler

    mail_handler = SMTPHandler(
        mailhost=(host, port),  # Mail host and port
        fromaddr=from_addr,  # From address
        toaddrs=to_addr_list,  # To address
        subject=subject,  # Subject line
        credentials=(username, password),  # Credentials
        secure=secure,
    )
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    # Log errors using: app.logger.error('Some error message')





