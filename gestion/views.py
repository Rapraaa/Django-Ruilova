from django.shortcuts import render, redirect, get_object_or_404 #que hace el object_or_404?
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required #permite que una funcion antes de ser ejecutada revise si estoy o no logeado
from django.utils import timezone
from django.conf import settings 
from .models import Autor #importara las variables del settings  #PQ ACA NO ES DJANGO.MODELS Y SOLO ES .MODELS??
# Create your views here.

def index(request): #llamamos o obetenmos como respuesta un request, osea va a devolver la info que nos de el navegador, cabezeras, cookies, etc
    title = settings.TITLE  #USARIA LA VARIABLE QUE CREAMOS EN SETTINGS, ENTONCES SI CAMBIAMOS SETTINGS CAMBIA RODO
    #llamamos el TITULO TAMBIEN
    #asi si cmabio en settings cambio en todo
    return render(request, "gestion/templates/home.html", {'titulo': title}) #EXPLICAR ESTO, \ explicar y practicar
#hay que crear la carpeta templates en gestion y el archivo index.html
#cuando no devuelva nada es el path raiz, cuando el path raiz sea ejecutada llama a la funcion index
#ahora vamos a crear los demas paths

def lista_libros(request):
    pass #para que es el pass aca

def crear_libro(request):
    pass

def lista_autores(request):
    autores = Autor.objects.all() #SELECT * FROM AUTORES #HAY QUE IMPORTAR EL AUTOR DEL MODELS PARA QUE LO RECONOZCA
    return render(request, 'gestion/templates/autores.html', {'autores' : autores} ) #explicar el render y quequest

def crear_autor(request):
    pass

def lista_prestamos(request):
    pass

def crear_prestamo(request):
    pass

def detalle_prestamo(request):
    pass

def lista_multa(request):
    pass

def crear_multa(request):
    pass

def pruebas(request):
    #se define para que sepa que es title
    title = settings.TITLE #de setings la variable title
    return render(request, "gestion/templates/pruebas.html", {'titulo': title})