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
from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView#librerias genericas para el views
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin #clae 11-12-25
from django.urls import reverse_lazy #clae 11-12-25



# Create your views here.

def index(request): #llamamos o obetenmos como respuesta un request, osea va a devolver la info que nos de el navegador, cabezeras, cookies, etc  #USARIA LA VARIABLE QUE CREAMOS EN SETTINGS, ENTONCES SI CAMBIAMOS SETTINGS CAMBIA RODO
    #el user.username ya se envia por defecto
    #llamamos el TITULO TAMBIEN
    #asi si cmabio en settings cambio en todo
    return render(request, "gestion/templates/home.html") #EXPLICAR ESTO, \ explicar y practicar
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
 
@login_required #TODO CREAR AUTOR Y EDITAR AUTOR JUNTOS PARA LOS DEMAS COSOS
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
        imagen = request.FILES.get('imagen') #es como el queset de imagen  pero se usa .files para archivos 
        if autor == None:
            Autor.objects.create(nombre=nombre, apellido=apellido, bibliografia=bibliografia, imagen=imagen) #EXPLICAR QUE HACE objects create
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
@login_required 
@permission_required('gestion.Ver_prestamos', raise_exception=True,) #hay que poner aparte del nombre del permiso de donde viene (gestion.)
def lista_prestamos(request): #el pass  se ponia para que bo de error por mientras
    Prestamos = Prestamo.objects.all() #SELECT * FROM AUTORES #HAY QUE IMPORTAR EL AUTOR DEL MODELS PARA QUE LO RECONOZCA
    return render(request, 'gestion/templates/prestamos.html', {'prestamos' : Prestamos} ) #eEL DE LA izquierda, el de comillas es el que se llama en html
 #el de la derecha es la variable que creamos
@login_required 
@permission_required('gestion.Gestionar_prestamos', raise_exception=True,) #SI NO PONEMOS raise_exepction true en vez de el error lo mandara al login 

#debe estar iniciado sesion y con permisos                                                                                 
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
            usuarios = get_object_or_404(User, id=usuarios_id) #estos se usan apra cuando es asi la lsita que se muestra
            #pq de la lista elegimos es el id recordemos, el value es su id, esto que guardamos es el id para  identifiacar
            #si lo que elegios realmente existe
            prestamo = Prestamo.objects.create(libro=libros, 
                                    usuario=usuarios, 
                                    fecha_prestamos=fechas_prestamos)
                                    #fecha_maxima=fechas_maximas) 
                                    #fecha_devolucion=fechas_devolucion)
            libros.disponible = False #como ay prestamo el libro ya no esta diponible
            libros.save()
            return redirect('lista_prestamos',) #id=prestamo.id) #luego para eidtar necesitare el id prestamo, por ahora asi esta bien
        #QUE HACE EL .id???? COMO FUNCIONA??
    fecha = (timezone.now().date()).isoformat # explciar esto QUE QUE EUQ?? expolicar
    #YYYY MM DD
    return render(request, 'gestion/templates/crear_prestamo.html', {'libros': libros, 
                  "usuarios" : usuarios,
                  'fecha' : fecha})   #EL ERRORE QUE TUVIMOS AHORITA FUE ACA, HAY QUE ABRIR LLAVE, PONER VALORES TODOS
# Y LUEGO CERRAR LLAVE, NO POENMOS ABRIR LALVE VALOR, CERRRAR LAVVE, COMO ABRIRR LLAVE, CERRAR, Y ASI, ESO ROMPE TODITO

def detalle_prestamo(request): #para editar o ver detalle, no se, aun falta
    pass

def lista_multa(request):
    multas = multa.objects.all() #SELECT * FROM AUTORES #HAY QUE IMPORTAR EL AUTOR DEL MODELS PARA QUE LO RECONOZCA
    return render(request, 'gestion/templates/multas.html', {'multas' : multas} ) #explicar el render y quequest
                                                    #este multas es el que se hace en el for para que saque los datos
def crear_multa(request):  
    prestamos = Prestamo.objects.filter(fecha_devolucion = None) #para no poder haer multas si ya devolvieron el libro, no tendria sentido

    if request.method == 'POST': #si quieren enviar
        prestamo_id = request.POST.get('prestamos') # el related name es prestamos#aca tenemos el id
        tipo = request.POST.get('tipo')

        if prestamo_id and tipo:
            prestamo = get_object_or_404(Prestamo, id=prestamo_id)
            #tipo = get_object_or_404(multa, id=tipo) al ser un choices no ahce falta            monto_calculado = prestamo.multa_retraso(tipo)
            multa.objects.create(
                prestamo=prestamo,
                tipo=tipo, 
            )
            return redirect('lista_multas')
    return render(request, 'gestion/templates/crear_multa.html', {'prestamos': prestamos})


def pruebas(request):
    #se define para que sepa que es title
    title = settings.TITLE #de setings la variable title
    return render(request, "gestion/templates/pruebas.html", {'titulo': title})


def registro(request): #"Hola, soy la función encargada del registro. Dame la carpeta de información del cliente
    #SI NO LO PONGO EN EL PARENSETISS NO VALE
    if request.method == 'POST':#Aquí el camarero abre la carpeta y mira una etiqueta que dice MÉTODO
    #GET: Significa "Solo vengo a mirar" (Ver la página).
    #POST: Significa "Vengo a entregar datos privados" (Enviar el formulario).
    #Traducción de la línea: "¿El usuario le dio clic al botón 'Enviar' o solo acaba de entrar a la página?"
        
        form = UserCreationForm(request.POST) #importamos para esto, #Crea un objeto formulario (form) usando el molde de registro, 
        #y rellénalo con los datos que escribió Juan (request.POST)
        if form.is_valid(): #¿Están bien los datos o Juan escribió tonterías?, que no sea repetido el usuario, que sean igual las contrase;as y asi
            usuario = form.save() #agarra los datos del formulario, conviértelos en una fila de SQL y guárdalos 
            #en la base de datos permanentemente. Y devuélveme al usuario creado en la variable usuario
            login(request, usuario)#ya que te acabas de registrar con éxito, te inicio sesión automáticamente ahora mismo para que entres directo

    else:
        form = UserCreationForm() #parentesis? para instanciarlo
    return render(request, 'gestion/templates/registration/registro.html', {'form':form}) #mandamos como parametro el formulario, como es eso de mandar
#parametros





#VISTA BASADA EN CLASES DE LIBRO
class LibroListView(LoginRequiredMixin, ListView): #vista basada en clases (MIXIN)
    model = Libro
    template_name = 'gestion/templates/libros_view.html' #es como el request
    context_object_name = 'libros' #este es el diccionario de libros que mandabamos, ES LO QUE ENVIAMSO AL HTML
    paginate_by = 1 #es para que se divida en paginas, osea que puedas aplastar 1, luego vas a la pagina 2
    #luego a la pagina 3, como en videos y asi, coge 10 datos y los otros 10 van a otra pagina

class LibroDetalleView(LoginRequiredMixin, DetailView):
    model = Libro
    template_name = 'gestion/templates/detalle_libros.html'
    context_object_name = 'libro'

class LibroCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Libro
    fields = ['titulo', 'autor', 'disponible']
    template_name = 'gestion/templates/crear_libros.html'
    success_url = reverse_lazy('libro_list') #cuando complete, cuando haga click en el boton de crear libro haga algo
    #el libro list es el nombre de la URL hay que rear otro para ver la diferencia entre asi y view normal
    permission_required = 'gestion.add_libro' #el permiso que django crea por defecto, aunque siempre podemos crear nosotros
    #TODO INVESTIGAR COMO SABER EL codename para el permiso que creeo django por defecto

class LibroUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Libro
    fields = ['titulo', 'autor']
    template_name = 'gestion/templates/editar_libros.html'
    success_url = reverse_lazy('libro_list')
    permission_required = 'gestion.change_libro'

class DeleteUpdateView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Libro
    template_name = 'gestion/templates/delete_libros.html' #un confirmar tipo, estas seguro de que quieres borrar el lalala
    success_url = reverse_lazy('libro_list')
    permission_required = 'gestion.delete_libro'

#ACA ACABA LA DE LIBRO