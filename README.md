# Flask-User starter app v1.0

This code base serves as starting point for writing your next Flask application.

This branch is for Flask-User v1.0.

For Flask-User v0.6, see [the Flask-User-Starter-App v0.6 branch](https://github.com/lingthio/Flask-User-starter-app/tree/v0.6).

## Code characteristics

* Tested on Python 2.6, 2.7, 3.3, 3.4, 3.5 and 3.6
* Well organized directories with lots of comments
    * app
        * commands
        * models
        * static
        * templates
        * views
    * tests
* Includes test framework (`py.test` and `tox`)
* Includes database migration framework (`alembic`)
* Sends error emails to admins for unhandled exceptions


## Setting up a development environment

We assume that you have `git` and `virtualenv` and `virtualenvwrapper` installed.

    # Clone the code repository into ~/dev/my_app
    mkdir -p ~/dev
    cd ~/dev
    git clone https://github.com/lingthio/Flask-User-starter-app.git my_app

    # Create the 'my_app' virtual environment
    mkvirtualenv -p PATH/TO/PYTHON my_app

    # Install required Python packages
    cd ~/dev/my_app
    workon my_app
    pip install -r requirements.txt


# Configuring SMTP

Copy the `local_settings_example.py` file to `local_settings.py`.

    cp app/local_settings_example.py app/local_settings.py

Edit the `local_settings.py` file.

Specifically set all the MAIL_... settings to match your SMTP settings

Note that Google's SMTP server requires the configuration of "less secure apps".
See https://support.google.com/accounts/answer/6010255?hl=en

Note that Yahoo's SMTP server requires the configuration of "Allow apps that use less secure sign in".
See https://help.yahoo.com/kb/SLN27791.html


## Initializing the Database

    # Create DB tables and populate the roles and users tables
    python manage.py init_db

    # Or if you have Fabric installed:
    fab init_db


## Running the app

    # Start the Flask development web server
    python manage.py runserver

    # Or if you have Fabric installed:
    fab runserver

Point your web browser to http://localhost:5000/

You can make use of the following users:
- email `user@example.com` with password `Password1`.
- email `admin@example.com` with password `Password1`.


## Running the automated tests

    # Start the Flask development web server
    py.test tests/

    # Or if you have Fabric installed:
    fab test


## Trouble shooting

If you make changes in the Models and run into DB schema issues, delete the sqlite DB file `app.sqlite`.


## See also

* [FlaskDash](https://github.com/twintechlabs/flaskdash) is a starter app for Flask
  with [Flask-User](https://readthedocs.org/projects/flask-user/)
  and [CoreUI](https://coreui.io/) (A Bootstrap Admin Template).

## Acknowledgements

With thanks to the following Flask extensions:

* [Alembic](http://alembic.zzzcomputing.com/)
* [Flask](http://flask.pocoo.org/)
* [Flask-Login](https://flask-login.readthedocs.io/)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/)
* [Flask-Script](https://flask-script.readthedocs.io/)
* [Flask-User](http://flask-user.readthedocs.io/en/v0.6/)

<!-- Please consider leaving this line. Thank you -->
[Flask-User-starter-app](https://github.com/lingthio/Flask-User-starter-app) was used as a starting point for this code repository.


## Authors

- Ling Thio -- ling.thio AT gmail DOT com

## Luke's comments below:

This was forked from https://github.com/lingthio/Flask-User-starter-app which is a flask-user app that uses the create_app
factory pattern.  In addition, it has the views modularized with blueprints and the models are in their own module as well.

Tips:

I. You can run this app using manage.py as the author recommends above.  This facilitates testing, migrations, and other stuff
not strictly related to smaller-scale development. As a result I find it easier to fire up the app with flask_app.py which the author added for PythonAnywhere integrations.  I added app.run() to that file.  So to fire up the app do:

>python flask_app.py

II. Originally I used to configure the email with an smtp.gmail.com address.  But that no longer seems to work.  So now I
use smtp.mailgun.org.  Visit the site to set up your own account.  It's free as long as one doesn't exceed sending 5000 emails.  The mailgun mail settings (server, port, mail username and mail password) are configured in local_settings.py  (This file is not included in the repo for security reasons)

III. The GUI has been stylized with bootstrap and a nav was added that includes an admin only link.  To get from the original forked code to this, the following steps were taken:

CUSTOMIZE FLASK_USER (https://flask-user.readthedocs.io/en/latest/customizing_forms.html)
  Create app/templates/flask_user folder
  Add templates to above folder from venv flask_user library
  Replace app/layout.html with one that contains nav links and bootstrap (modify paths in nav slightly)
  Modify app/flask_user/common_base so it extends layout.html instead of flask_user_layout

Modified the contents of main/admin_page, main/home_page, main/main_base, main/user_page. (they still extend main_base)

Took context processor that allows isAdmin function to run in nav template and placed it in app/_init_.py/create_app function.  (If you leave it in the blueprint it wont be available to the flask_user views)

In local_settings I changed the value of USER_APP_NAME = "Luke's App".  The variable (and many others) are loaded with a
context processor in the app_create function into the user_manager variable.  It is then accessed in the templates with {{ user_manager.USER_APP_NAME }}


