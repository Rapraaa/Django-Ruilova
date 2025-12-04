from django.shortcuts import render, redirect, get_object_or_404 #que hace el object_or_404?
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required #permite que una funcion antes de ser ejecutada revise si estoy o no logeado
from django.utils import timezone
from django.conf import settings 
from .models import Autor, Libro, Prestamo, multa#importara las variables del settings  #PQ ACA NO ES DJANGO.MODELS Y SOLO ES .MODELS??
# Create your views here.

def index(request): #llamamos o obetenmos como respuesta un request, osea va a devolver la info que nos de el navegador, cabezeras, cookies, etc
    title = settings.TITLE  #USARIA LA VARIABLE QUE CREAMOS EN SETTINGS, ENTONCES SI CAMBIAMOS SETTINGS CAMBIA RODO
    #llamamos el TITULO TAMBIEN
    #asi si cmabio en settings cambio en todo
    return render(request, "gestion/templates/home.html", {'titulo': title}) #EXPLICAR ESTO, \ explicar y practicar
#hay que crear la carpeta templates en gestion y el archivo index.html
#cuando no devuelva nada es el path raiz, cuando el path raiz sea ejecutada llama a la funcion index
#ahora vamos a crear los demas paths

####################################
### LIBROSSSS ####################
################################
def lista_libros(request):
    libros = Libro.objects.all() 
    return render(request, 'gestion/templates/libros.html', {'libros' : libros} ) 

def crear_libro(request): #hay que sacar los autores pq los necestiamos para que??
    autores = Autor.objects.all() #select * from autor
    #necesitamos los autores auqnue sea libros para poder hacer las opcioens de los autores con las que ya tenemos
    #asi es, entonces digamos que por asi decirl as relaciones hay que llamarlas asi con el select *

    if request.method == "POST":
        titulo = request.POST.get('titulo')
        autor_id = request.POST.get('autor_id')
                                              
        if titulo and autor_id:    #si tengo titulo y id es que ya selecciono un libro, ahora un filtro 
            autor = get_object_or_404(Autor, id=autor_id) #si no obitnee el error da un error 404
            Libro.objects.create(titulo=titulo, autor=autor) #los guarda en la lista, los crea en la base de datos
            return redirect('lista_libros')
    return render(request, 'gestion/templates/crear_libros.html' , {'autores' : autores}) #qie ahce la comilla aca, pq uno tiene comilla y el otro no
#aca al hacer el render del crear libro si tenemos que enviar un parametro, que serai el autores, pq para crear un libro necesitas los autores
#aca en el ultimo return me dio un error por no poner bien la identacion, y los parentesis, OJO
####################################3



def lista_autores(request):
    autores = Autor.objects.all() #SELECT * FROM AUTORES #HAY QUE IMPORTAR EL AUTOR DEL MODELS PARA QUE LO RECONOZCA
    return render(request, 'gestion/templates/autores.html', {'autores' : autores} ) #explicar el render y quequest
 
def crear_autor(request):       #EXPLICAER QUE ES UN METODO POST
    if request.method == 'POST': #QUE HACE REQUEST Y POST?????????????
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')   #ES UNO POR CADA UNO
        bibliografia = request.POST.get('bibliografia')  #lo que hace es sacar o guardar en una variable lo que saquemos de nuestro HTML
        Autor.objects.create(nombre=nombre, apellido=apellido, bibliografia=bibliografia) #EXPLICAR QUE HACE objects create
        #nombre de autor es nombre de aca, autor de autor es auator de aca y asi
        return redirect('lista_autores') #redirecciona a lista autores para que lo liste, osea cada que crees un usuario te va a llevar alla
    return render(request, 'gestion/templates/crear_autor.html', ) #si no es un metodo POST Y SOLO ESTA CARGANDO los datos se va al crear libros
    #los metodos SE VEN CON EL INSPECCIONAR ESE RARO EN NETWORK


def lista_prestamos(request): #el pass  se ponia para que bo de error por mientras
    Prestamos = Prestamo.objects.all() #SELECT * FROM AUTORES #HAY QUE IMPORTAR EL AUTOR DEL MODELS PARA QUE LO RECONOZCA
    return render(request, 'gestion/templates/prestamos.html', {'prestamos' : Prestamos} ) #eEL DE LA izquierda, el de comillas es el que se llama en html
                                                                                            #el de la derecha es la variable que creamos
def crear_prestamo(request):
    #libros = Libro.objects.all #sacamos todos los datos del libro
    #EL METODO GET ES CUANDO BSUCAAS ALGO Y EL OBTIENES ALGO DE L SERVIDOR
    #EL METODO PSOT ES CUANDO LE DAS UNA INFORAMCION AL SERVIDOR PARA QUE ESE HAGA ALGO CON ELLA
    #if request.method == 'POST': #buscar como consigue request method el metodo
        #libro = request.POST.get('libro')
    pass

def detalle_prestamo(request):
    pass

def lista_multa(request):
    multas = multa.objects.all() #SELECT * FROM AUTORES #HAY QUE IMPORTAR EL AUTOR DEL MODELS PARA QUE LO RECONOZCA
    return render(request, 'gestion/templates/multas.html', {'multas' : multas} ) #explicar el render y quequest
                                                    #este multas es el que se hace en el for para que saque los datos
def crear_multa(request):  
    pass

def pruebas(request):
    #se define para que sepa que es title
    title = settings.TITLE #de setings la variable title
    return render(request, "gestion/templates/pruebas.html", {'titulo': title})