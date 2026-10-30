from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from django.db.backends.mysql.base import DatabaseWrapper
        
        DatabaseWrapper.check_database_version_supported = lambda self: None
        from django.db.backends.mysql.features import DatabaseFeatures
        DatabaseFeatures.can_return_columns_from_insert = False
        DatabaseFeatures.can_return_rows_from_bulk_insert = False