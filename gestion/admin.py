from django.contrib import admin
from .models import Autor, Prestamo, Libro, multa, SolicitudPrestamo
# Register your models here.

admin.site.register(Autor)  #paraa ver los autores en la pagina de adminstracion, es necesario importar el obketo o modulo tambien con
#from .models import Autor

admin.site.register(Prestamo)

admin.site.register(multa)

admin.site.register(SolicitudPrestamo)

#admin.site.register(Libro)

@admin.register(Libro)  #SI LO PONGO DE ESTA FORMA EN VEZ DE ESTAR EL NOMBRE DEL STR Y HACERLE CLICK PARA VER LO DEMAS SALE DE POR SI COMO UN EXCEL
class Libro_admin(admin.ModelAdmin): #en lugar de usar la clase de models, uso una version modificada para admin
    list_display = ('titulo', 'autor', 'disponible')
#esta clase solo dice como va a mostrar los datos, y como tiene el decorador del admin register ya sabe que se usa para el Libro original
#es coko que libro es la comida y libro_Admin el menu


#admin.site.register si no voy a cambiar nada 
#@admin.register(Libro)  si voy a modificar el como se ve 