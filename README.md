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

#Docker

Run:
    
    create directory "media" !!!
    create file boot.sh with:

        #!/bin/bash
        source venv/bin/activate
        export MAIL_SERVER=smtp.googlemail.com
        export MAIL_PORT=587
        export MAIL_USE_TLS=1
        export MAIL_USERNAME=<your-gmail-email>
        export MAIL_PASSWORD=<your-gmail-password>
        export ADMINS=<admin1>#<admin2>#...
        flask db upgrade
        flask createsuperuser username_password_email
        exec gunicorn -b :5000 --access-logfile - --error-logfile - ecommerce:app

    docker build -t ecommerce:latest .
    
    docker run --name ecommerce -d -p 8000:5000 --rm ecommerce:latest
