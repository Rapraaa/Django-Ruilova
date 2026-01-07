from django.contrib import admin
from .models import Autor, Prestamo, Libro, multa, SolicitudPrestamo
# Register your models here.
from simple_history.admin import SimpleHistoryAdmin
admin.site.register(Autor, SimpleHistoryAdmin)  #paraa ver los autores en la pagina de adminstracion, es necesario importar el obketo o modulo tambien con
#from .models import Autor

admin.site.register(Prestamo, SimpleHistoryAdmin)

admin.site.register(multa, SimpleHistoryAdmin)

admin.site.register(SolicitudPrestamo, SimpleHistoryAdmin)

#admin.site.register(Libro)

@admin.register(Libro)  #SI LO PONGO DE ESTA FORMA EN VEZ DE ESTAR EL NOMBRE DEL STR Y HACERLE CLICK PARA VER LO DEMAS SALE DE POR SI COMO UN EXCEL
class Libro_admin(SimpleHistoryAdmin): #en lugar de usar la clase de models, uso una version modificada para admin
    list_display = ('titulo', 'autor', 'disponible')
#esta clase solo dice como va a mostrar los datos, y como tiene el decorador del admin register ya sabe que se usa para el Libro original
#es coko que libro es la comida y libro_Admin el menu


#admin.site.register si no voy a cambiar nada 
#@admin.register(Libro)  si voy a modificar el como se ve 


@admin.register(Libro.history.model) #para ber todos los registros  de libros en el admin, jala el modelo del historial, se crea solo con la libreria
class LibroHistoryAdmin(admin.ModelAdmin):
    # Definimos qué columnas ver en la auditoría global
    list_display = ('history_date', 'history_user', 'history_type', 'titulo', 'autor')
    
    # history_type suele ser '+' (crear), '~' (editar) o '-' (borrar), son filtros a la derecha para filtrar
    list_filter = ('history_type', 'history_date', 'history_user')
    
    # Ordenamos del cambio más reciente al más antiguo
    ordering = ('-history_date',)