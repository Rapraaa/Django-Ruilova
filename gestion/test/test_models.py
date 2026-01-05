from django.test import TestCase
#PARA TESTEOS
from gestion.models import Libro, Autor, Prestamo #los uqe vamos a testear
from django.contrib.auth.models import User  #NECESITAMOS EL USER PARA LOS PRESTAMOS
from django.utils import timezone
from django.urls import reverse 

class LibroModelTest(TestCase): #cada clase es un test
    @classmethod #  TODO EXPLICAR QUE HACE EL CLASS METHOD, que es class methooooooood

    def setup_test_data(cls): #todo datos pal test, TODO que es cls que es cls 
        autor = Autor.objects.create(nombre="Isaac", apellido='Asimov', bibliografia='bacan')
        Libro.objects.create(titulo="fundacion", autor=autor, disponible=True)
        #si necesitara testear algo ams ahi si lo guardo en una variavbvle, sino solo lo guardo asi nomas pq lbiro es el ultimo paso
        #explicar esto mejor
        #ESTENDER CUANDO PONER EN UNA VARIABLE Y CUANDO NO
    def test_str_devuelve_titulo(self): #TODO XPLCIAR TODO ESTO DE LOS TEST, SE PARECEN AL CODEWARS
        libro = Libro.objects #y pq aca se usa la bariavle
        #si ponemos self. ahi se autocompletan con el monton de test que hay
        #en internet ver que mas test hay que me sirvan
        self.assertEqual(str(libro), 'fundacion') #deberia dar error por que el __str__ del models es titulo + autor

        #si cambiamos el str para que solo de el titulo saldra bien

#CLASE PARA PROBAR UN PRESTAMO
class PrestamoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls): #pongo setupte se completa solo
        usuario = User.objects.create(username='Juan', password='#123UTEpro') #en la linea de abajo pusimos autor=1 [[ara poner el id, pero asi no sirve y dio error
        #para pasar bien el id del autor debemos poner autor_id=1
        libro = Libro.objects.create(titulo='I Robot', autor_id=1, disponible=True) #pq aca si ponemos en variabl
        #TODO el autor id me esta dando error, no encuentra el autor id 1, arreglar
        #pq el cls prestamo el test es para todos los daots que metemos a la variable libro, y sino el setup tendriamos que ahcer dentro de donde pondriamos
        #libro y es mas bola y desorganizado
        cls.prestamo = Prestamo.objects.create(  #todo que es esto de cls.prestamo
        libro=libro,
        usuario = usuario,
        fecha_maxima = '2025-12-25') #tendriamso que pone fcha maxima es igual a nuestra funcion pasa sacar fecha mxima

        #PROBEMOS A NO PONER LA FECHA esa que es un dato obligatorio para ver que pasa
        #dara un error de not null fecha max
    def test_libro_no_disponible(self):
        self.prestamo.refresh_from_db() #que hace refresh from db
        self.assertFalse(self.prestamo.libro.disponible)
        #self.assertEqual(self.prestamo.dias_retraso, 0)    
       # if self.prestamo.dias_retraso > 0:
        #COMPLETAR EL TEST DE DIAS RETRASOS      

class PrestamoUsuarioViewTest(TestCase):
    def setUp(self): #que pasas si solo hago setup y no setup data
        self.user1 = User.objects.create_user('u1', password='test12345') #EXPLICAR ESSTO, COMO ASI QUE USAER 1, U1 Y TODO ESTO
        self.user2 = User.objects.create_user('u2', password='test12345')   
            
    def test_redirige_no_login(self):
        resp = self.client.get(reverse('crear_autor'))     
        self.assertEqual(resp.status_code, 302)  #si le cambiara por 200, osea que si sirva va a dar falso, pq da un 302, osea ma redirecciona aunque yo espero el 200
         #explciar el status code #como queremos entrar al crear autor si no estamos logeado debe mandarnos a la pagina de login
        #entonces el status code nos dira si si encontro otra pagina
        #EPLICACION CODIGOS DE STATUS CODE
        #https://developer.mozilla.org/es/docs/Web/HTTP/Reference/Status ----------------------------------
        #CODIGOS de estado de respuesta http BUSCAR EN GOOGLE TODO
        #segun la respyesta desde el 100 al 199 son respuestas informativas
        #sastisfactorias van del 200 al 299
        #redireccion es del 300 al 399
        #errores de clientes, osea ingreso de datos o asi que tieneen que ver con el cliente 400 a 499
        #errorres del servidor 500 a 599
     #hay com oahcer que se vea mas bonito?

    def test_carga_login(self):
        resp =self.client.login(username='u1', password='test12345')
        #self.assertEqual(resp.status_code, 200) #el def lo definimos antes aca la respuesta es como tal un true o false, explicar eso, como asi que es un true o false
        resp1=self.client.get(reverse('crear_autor'))     
        self.assertEqual(resp1.status_code, 200)