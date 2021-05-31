# Flask ecommerce

Installing:

    python3 -m venv DirectoryVENV
    source DirectoryVENV/bin/activate
    pip install -r requirements.txt
    flask db migrate
    flask db upgrade
    export FLASK_APP=ecommerce.py
    export FLASK_ENV=development (or production)
    export FLASK_DEBUG=1 (or 0 (production))
    flask createsuperuser username_password_email (create superuser)
    flask run
