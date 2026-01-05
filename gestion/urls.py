from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views #ESTO NECESITAMOS IMPORTAR PARA LO DEL LOGIN Y CAMBIO DE CONTRASE;A, EXPLICAR IGUALLLLLLLLLLLLLLLL
#ALLLLLLLLLLLL
from django.contrib.auth.decorators import login_required #NECESARIO PARA EL LOGIN REQUIRED ES UN DECORADOR

urlpatterns = [ 
    path("", index, name="index"),#por ahora va a dar error pq aun no creamos en views ninguna vista
    #el path es la URL que ponemos en el navegador
    #el path principal es digamos google.com y el path secundario es el /serach hachahcajsdasd y asi
    #LIBROS

#EL PRIMER PATH NOS LLEVARA A UN INDEX, OSEA EN VEZ DE LA DE DJANGO SERA UNA PROPIA DE NOSOTROS


    #LOGIN
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'), #el next page le dices a donde

    #cambio de contraSE;A
    path('password/change', auth_views.PasswordChangeView.as_view(), name='password_change'), #PQ SE DEBEN LLAMA ASI, QUE HACEN REALMENTE EXPLICAR TODOO
    path('password/change/done', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),  #TODITO LO DEL LOGIN ENTENDER

    #registro

    path('registro/', registro, name="registro"), #oq aca mno usamos auth views y arriba si, entender lo del auth bviews


    # LIBROS PRESTAMOS Y TODOO ESO
    path('libros/', lista_libros, name="lista_libros"),
    path('libros/nuevo/', crear_libro, name="crear_libro"),
    #AUTORES
    path("autores/", lista_autores, name="lista_autores"),
    path("autores/nuevo/", crear_autor, name="crear_autor"),
    path("autores/<int:id>/editar/", crear_autor, name="editar_autores"),
    #PRESTAMOS
    path("prestamos/", lista_prestamos, name="lista_prestamos"),
    path("prestamos/nuevo/", crear_prestamo, name="crear_prestamo"),

    #path("prestamos/<int:id>", detalle_prestamo, name="detalle_prestamo"),#el int id hace #EXPLICARA ESTOOO
    #MULTAS
    path('multas/', lista_multa, name="lista_multa"),
    path('multas/nuevo', crear_multa, name="crear_multa"), #hay que ponerle relacion con prestamos
    #PRUEBAS
    path("pruebas/", pruebas, name="pruebas"), #A QUE LLAMA EL SEUGNDO NOMBRE? EL PATH EL ANTES DE LNAME
#explicar que hace lo del int id

    #PATHS NUEVOS PARA LA VISTA BASADDA EN CLASE DE LIBROS
    path('libro_list/', LibroListView.as_view(), name='libro_list'), #el as view es pq en realidad es una clase, y hay que hacer que la detecten como vista
    #investigar mas lo del as view
    #QUE HAY QUE PONER EN EL NAME
    path('multas/pagar/<int:multa_id>/', pagar_multa, name='pagar_multa'), #PARA PAGAR MULTAS ANTENTOTJAIOJDASD
    path('prestamos/devolver/<int:prestamo_id>/', devolver_libro, name='devolver_libro'), #DEVOLVER LIBRO
]  #hay que poner el mismo crear autor para los 2

#enlazar prestamo a la multa
#ACA ESTAMOS CREANDO LOS URL QUE VAMOS A MANEJAR, EN ESE CASO SERIA LOCALHOST/LIBROS Y LLAMARA AL PATH DE LIBROS Y ASI CON TODO
 #en view hay que crear las funcionalidades que seran llamadas por las urls
#nos llevaria a la funcion esa en blanco, el lista libros por ejemplo

