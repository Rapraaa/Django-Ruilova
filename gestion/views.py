from django.shortcuts import render, redirect, get_object_or_404 #que hace el object_or_404?
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required #permite que una funcion antes de ser ejecutada revise si estoy o no logeado
from django.utils import timezone
from django.conf import settings 
from .models import Autor, Libro, Prestamo, multa#importara las variables del settings  #PQ ACA NO ES DJANGO.MODELS Y SOLO ES .MODELS??
from django.http import HttpResponseForbidden #para que lleve al forbiden
from django.contrib.auth.forms import UserCreationForm #EES EL FORMULARIO PARA CREAR USUARIOS QUE YA VIENE CON DJANGO
#PARA NO TENER QUE CREARLO NOSOTROS MISMOS
from django.contrib.auth import login #el login que usamos para crear usuarios

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
 
@login_required
def crear_autor(request, id=None): #le pedimos el id pero puede ser none? #EXPLICAR #si el id no tiene valor sale con none
     #aca pedimos el parametro request, ya que sin request no hay como saber si es post o no                
    #EXPLICAER QUE ES UN METODO POST
    if id == None: # si la id no existe
        autor = None #para que es esto?
        modo = 'Crear' #una bandera
    else:
        autor = get_object_or_404(Autor, id=id)
        modo = 'Editar'

    if request.method == 'POST': #QUE HACE REQUEST Y POST?????????????
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')   #ES UNO POR CADA UNO
        bibliografia = request.POST.get('bibliografia')  #lo que hace es sacar o guardar en una variable lo que saquemos de nuestro HTML

        if autor == None:
            Autor.objects.create(nombre=nombre, apellido=apellido, bibliografia=bibliografia) #EXPLICAR QUE HACE objects create
            return redirect('lista_autores')
        else:
            autor.nombre = nombre #EXPLICAR ESO
            autor.apellido = apellido
            autor.bibliografia = bibliografia
            autor.save()  #EXPLICAR POR QUE LA A DEBE SER MINUSCULA
        #nombre de autor es nombre de aca, autor de autor es auator de aca y asi
            return redirect('lista_autores') #PARA QUE SIRVE ESTE RREDIRECT???
        #redirecciona a lista autores para que lo liste, osea cada que crees un usuario te va a llevar alla
        #mandar los daatos del titulo o del boton
    context = {'autor':autor,
               'titulo': 'Editar Autor' if modo == 'Editar' else 'Crear Autor',
               'texto_boton': 'Guardar cambios' if modo == 'Editar' else 'Crear'} #acasdasd
    return render(request, 'gestion/templates/crear_autor.html', context ) #les mandamos el contexto #REVISAR BIEN ESTO
    #como funciona eso??
    #  #si no es un metodo POST Y SOLO ESTA CARGANDO los datos se va al crear libros
    #los metodos SE VEN CON EL INSPECCIONAR ESE RARO EN NETWORK

#def  editar_autor(request, id): #hay que mandar el autor en el return para poder visualizar los datos
 #   autor = get_object_or_404(Autor, id = id) #que siempre coincida con la id que nos manda la pagina
  #  if request.method == 'POST':
   #     nombre = request.POST.get('nombre')
    #    apellido = request.POST.get('apellido')   #ES UNO POR CADA UNO
     #   bibliografia = request.POST.get('bibliografia')   
      #  if nombre and apellido:
       #     autor.nombre = nombre #EXPLICAR ESO
        #    autor.apellido = apellido
         #   autor.bibliografia = bibliografia
          #  autor.save()  #EXPLICAR POR QUE LA A DEBE SER MINUSCULA
       # return redirect('lista_autores')
   # return render(request, 'gestion/templates/editar_autor.html', {'autor' : autor})
def lista_prestamos(request): #el pass  se ponia para que bo de error por mientras
    Prestamos = Prestamo.objects.all() #SELECT * FROM AUTORES #HAY QUE IMPORTAR EL AUTOR DEL MODELS PARA QUE LO RECONOZCA
    return render(request, 'gestion/templates/prestamos.html', {'prestamos' : Prestamos} ) #eEL DE LA izquierda, el de comillas es el que se llama en html
 #el de la derecha es la variable que creamos
@login_required     #COMO USAR ESTO CORRECTANEBTE                                                                                     
def crear_prestamo(request): 
   # if not request.user.has.perm(gestion.Gestion_prestamos):
    #    return HttpResponseForbidden() #from django.http import HttpResponseForbidden
    #libros = Libro.objects.all #sacamos todos los datos del libro
    #enves de objects all podemos usar filter
    libros = Libro.objects.filter(disponible = True) #mejor que todos, solo dan los disponibles
    usuarios = User.objects.all() #DE DONDE VIENE ESTE USER_ COMO LO USO_ PARA QUE SIRVE? COMO LO VEO O EDITO?
    #EL METODO GET ES CUANDO BSUCAAS ALGO Y EL OBTIENES ALGO DE L SERVIDOR
    #EL METODO PSOT ES CUANDO LE DAS UNA INFORAMCION AL SERVIDOR PARA QUE ESE HAGA ALGO CON ELLA
    if request.method == 'POST': #buscar como consigue request method el metodo
                              #si es que el metodo es post
        libros_id = request.POST.get('libro')
        usuarios_id = request.POST.get('usuario')  #QUE PASA SI PONGO EL NOMBRE DE LA VARIABLE ACA EL MISMO DE ARRIBA DEL USER.OBJECTS.ALL
        fechas_prestamos = request.POST.get('fecha_prestamos')
        #fechas_maximas_id = request.POST.get('fecha_maxima') #se hace automatico no hace falta
        #fechas_devolucion = request.POST.get('fecha_devolucion')  #automatico
        if libros_id and usuarios and fechas_prestamos: #si ya existe, osea asi no lleno en blanco
            libros = get_object_or_404(Libro, id=libros_id)
            usuarios = get_object_or_404(User, id=usuarios_id)
            prestamo = Prestamo.objects.create(libro=libros, 
                                    usuario=usuarios, 
                                    fecha_prestamos=fechas_prestamos)
                                    #fecha_maxima=fechas_maximas) 
                                    #fecha_devolucion=fechas_devolucion)
            libros.disponible = False
            libros.save()
            return redirect('lista_prestamos', id=prestamo.id) #EXPKCIAER ACCA, INVEESTIGAR ESTO HASTA ENTENDER TODITO COMPLETAMENTE
        #QUE HACE EL .id???? COMO FUNCIONA??
    fecha = (timezone.now().date()).isoformat # explciar esto QUE QUE EUQ?? expolicar
    #YYYY MM DD
    return render(request, 'gestion/templates/crear_prestamo.html', {'libros': libros, 
                  "usuarios" : usuarios,
                  'fecha' : fecha})   #EL ERRORE QUE TUVIMOS AHORITA FUE ACA, HAY QUE ABRIR LLAVE, PONER VALORES TODOS
# Y LUEGO CERRAR LLAVE, NO POENMOS ABRIR LALVE VALOR, CERRRAR LAVVE, COMO ABRIRR LLAVE, CERRAR, Y ASI, ESO ROMPE TODITO

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

def registro(request): #EXPLICAR TODITO ESTO DE 0, ENTENDERLO BIEN #EXPLICAR ESO DEL REQUEST, NO ENTIEND OQEU ES NI COMO FUNCIONA
    #SI NO LO PONGO EN EL PARENSETISS NO VALE
    if request.method == 'POST':
        form = UserCreationForm(request.POST) #importamos para esto
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)

    else:
        form = UserCreationForm
    return render(request, 'gestion/templates/registration/registro.html', {'form':form}) #mandamos como parametro el formulario, como es eso de mandar
#parametros

