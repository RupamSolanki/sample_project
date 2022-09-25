from django.apps import AppConfig
from django.db.models.signals import post_migrate

class DbAppConfig(AppConfig):
    """
    Class to Configure the app.
    """
    name = 'db'

    def ready(self):
        import db.signal
        post_migrate.connect(db.signal.populate_groups, sender=self)
        post_migrate.connect(db.signal.populate_users, sender=self)
        post_migrate.connect(db.signal.populate_books, sender=self)
