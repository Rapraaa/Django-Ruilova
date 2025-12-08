from django.urls import path
from .views import *

urlpatterns = [ 
    path("", index, name="index"),#por ahora va a dar error pq aun no creamos en views ninguna vista
    #el path es la URL que ponemos en el navegador
    #el path principal es digamos google.com y el path secundario es el /serach hachahcajsdasd y asi
    #LIBROS

#EL PRIMER PATH NOS LLEVARA A UN INDEX, OSEA EN VEZ DE LA DE DJANGO SERA UNA PROPIA DE NOSOTROS

    path('libros/', lista_libros, name="lista_libros"),
    path('libros/nuevo/', crear_libro, name="crear_libro"),
    #AUTORES
    path("autores/", lista_autores, name="lista_autores"),
    path("autores/nuevo/", crear_autor, name="crear_autor"),
    path("autores/<int:id>/editar/", crear_autor, name="editar_autores"),
    #PRESTAMOS
    path("prestamos/", lista_prestamos, name="lista_prestamos"),
    path("prestamos/nuevo/", crear_prestamo, name="crear_prestamo"),

    path("prestamos/<int:id>", detalle_prestamo, name="detalle_prestamo"),#el int id hace #EXPLICARA ESTOOO
    #MULTAS
    path('multas/', lista_multa, name="lista_multa"),
    path('multas', crear_multa, name="crear_multa"), #hay que ponerle relacion con prestamos
    #PRUEBAS
    path("pruebas/", pruebas, name="pruebas"), #A QUE LLAMA EL SEUGNDO NOMBRE? EL PATH EL ANTES DE LNAME
#explicar que hace lo del int id
]  #hay que poner el mismo crear autor para los 2

#enlazar prestamo a la multa
#ACA ESTAMOS CREANDO LOS URL QUE VAMOS A MANEJAR, EN ESE CASO SERIA LOCALHOST/LIBROS Y LLAMARA AL PATH DE LIBROS Y ASI CON TODO
 #en view hay que crear las funcionalidades que seran llamadas por las urls
#nos llevaria a la funcion esa en blanco, el lista libros por ejemplo