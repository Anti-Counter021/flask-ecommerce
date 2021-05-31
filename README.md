# Flask ecommerce

Installing { (text) - instruction }:

    python3 -m venv DirectoryVENV
    source DirectoryVENV/bin/activate
    pip install -r requirements.txt
    create directory "media"
    export FLASK_APP=ecommerce.py
    export FLASK_ENV=development (or production)
    export FLASK_DEBUG=1 (or 0 (production))
    create config.env and export:
        SECRET_KEY=<SECRET_KEY>
        MAIL_SERVER=smtp.googlemail.com
        MAIL_PORT=587
        MAIL_USE_TLS=1
        MAIL_USERNAME=<your-gmail-email>
        MAIL_PASSWORD=<your-gmail-password>
        ADMINS=<admin1>#<admin2>#...
    flask db migrate
    flask db upgrade
    flask createsuperuser username_password_email (create superuser)
    flask run
