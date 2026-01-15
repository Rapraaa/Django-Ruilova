from django.apps import AppConfig


class GestionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion'

    def ready(self): #esto se ejecuta solo cuando ya cargo todo, si pusiera el import arriba cargaria eso de signals antes de que cargue todo y peta
        import gestion.signals #importamos el archivo signals
#ACA ES DONDE DECIMOS QUE COSAS DEBE LEER
#Inusable esot ya, borrar