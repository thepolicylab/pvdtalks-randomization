from pvdtalks.app import create_app
from pvdtalks import tasks

app, celery = create_app()
