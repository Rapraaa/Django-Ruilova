from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import Permission #NECESARIO PARA LOS PERMISOS AUTOMATICOS 
from django.dispatch import receiver #PARA LOS PERMISOS AUTOMATICOS
from django.db.models.signals import post_save #para los permisos automartico, se ejecuta despues de guardarse
from django.contrib.auth.models import User, Group #para los usuarios  y grupos y permisos automaricos
from datetime import datetime #para convertir string a fecha

# Create your models here.
class Autor(models.Model): #parecido a django, 
#aca ya no necesitamos eso del guion bajo name, description nada de eso
    nombre = models.CharField(max_length=50) #models es tipo texto y tiene un maximo de caracteres de 50
    apellido = models.CharField(max_length=50) #lo mismo pero para apellido
    bibliografia = models.CharField(max_length=200, blank=True, null=True)
#HAY QUE QUE ELEGIR CUAL VA A SER EL "NAME" por asi decir, el que sea el nombre o representante de la clase o objeto. en odoo usabamos el recname
#o el display name, aca en django lo que ahcemos es lo siguiente
    def __str__(self): #por que se pone __ ?????????????????????????????????????????????????????
        return f"{self.nombre} {self.apellido}" #aca nos va a devolver como NOMBRE DEL OBJETO el nombre, espacio apellido
    
class Libro(models.Model): #clase para el libro
    titulo = models.CharField(max_length=20)
    #ACA TENEMOOS QUE HACER UNA RELACION, ACA NO HAY MANY2ONE COMO EN ODOO, ACA SE DEFINE DE UNA CON FOREIGN KEY, LO VOLVEMOS LALVE FORANEA
    autor = models.ForeignKey(Autor, related_name="libros", on_delete=models.PROTECT) #TAMBIEN DEBEMOS DEFINIR DE QUIEN ES LA LALVE FORANEA, en este caso de autor, tambien hay que
    #definir un related name
    #siempre en una foreign key hay que poner el ON DELETE, es decirle que hacer cuando alguien queira borrarlo, ya que tiene
    #relaciones y se podria romper segun lo que haga, digamos si borro el libro, los que tieenen prestado ese libro ya quedarian incompletos en su tabla
    #y se podrian romper cosas, pr eso hay que definir que hacer al borrar una llave foranea
    #el ON DELETE PROTECT lo que hace es proteger el registro apra que no sea eliminado
    #PARA QUE ES EL RELATED NAME???????????????????????????????????????????????????????????????
    #NUNCA OLVIDAR EL DEF STR
    disponible = models.BooleanField(default=True) #un boolean y por defecto viene acctivado
    def __str__(self):
        return self.titulo
    
class Prestamo(models.Model):
    libro = models.ForeignKey(Libro, related_name="prestamos", on_delete=models.PROTECT) #llave foranea con la clase de libros, prestamo y libros
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="prestamos", on_delete=models.PROTECT)  #PARA MANEJAR USUARIOS NECESITAMOS IMPORTAR UNA LIBRERIRA, asi "from django.conf import settings" importamos
    #settins acca, necesitamos el tema del auth
    #sacamos el auth_user_model, desde donde? desde settings,
    #QUE HACE EL AUTH USER MODEL ???????????????????????????????????????????????????/
    fecha_prestamos = models.DateField(default = timezone.now) #TENEMOS QUE IMPORTAR LA LIBRERIA DE TIMEZOMNE "from django.utils import timezone"
    #para fechas hay datetime field, y el date field, uno no usa hora
    fecha_maxima = models.DateField()
    fecha_devolucion = models.DateField(blank=True, null=True) 
    #EN DJANGO, POR DEFECTO TODOS LOS CAMPOS QUE QUEREMOS VAN A SER OBLIGATORIOS, aca no hay que poner el required = true, siempre seran obligatorios
    #si quieres que no sean obligatorios hay que poner "blank=True y null=True" asi permite registros blancos y nulos
    
    class Meta: #PARA LA METADADDA, APRENDER POO PARA VER QUE ES ESTO DE UN CLASS DEONTRO DE OTRO CLASS
        permissions= {
            ("Ver_prestamos", "Puede_ver_prestamos"),
            ("Gestionar_prestamos", "Puede_gestionar_prestamos")
        }
        
    def __str__(self):
        return f"prestamo de {self.libro} a {self.usuario}" #se usan CORCHETES, aca cramos un mensaje para el nombre del objeto
    
    #ATENTOS, HACEMOS ACA ESTO PARA QUE SIRVA DE DONE SEA QUE SE CREE EL USUARIO, NO SOLO DE LA PAGINA WEB

    @receiver(post_save, sender=User) #que se ejecute solo despues de que se guarde algo, con el sender le decimos que ese algo es un usuario
    def dar_permisos(sender, instance, created, **kwargs): #SENDER = Quién envió la señal (La clase User)
        #instance: EL DATO CLAVE. Es el usuario específico que se acaba de crear (ej: "Juan Pérez")
        #created: Un semáforo (Verdadero o Falso). Nos dice: "¿este usuario se acaba de crear hoy o solo modifico algo?"
        #kwargs es como una bolsa que guarda cualquier otro dato que envie y que no necesitemos para evitar error, pq el psot save puede mandar mas cosas
        #por ejemplo si en alguna parte guardo en el usuario con un update fields se damiaria si no uso el kwargs
        if created: #si fue creado y no modificado
            try: #va a intentar esto
                grupo = Group.objects.get(name='Usuario(prestamos)') #saca en la variable grupos el grupo de usuario prestamos que cree desde admin

                instance.groups.add(grupo) #a la instancia (el usuario que se creo) le va a agregar ese grupo

            except Group.DoesNotExist: #si por algun motivo falla (que no deberia)
                pass #no hace nada xd


    #AHORA VAMOS A CREAR LAS FUNCIONES PARA LA FECHA MAXIMA, MULTAS Y ASI
    #VAMOS A USAR ALGUNOS CONSTRUCTORES, ESTOS NOS PERMITEN TRABAJAR CON LAS PROPIEDADES O ATRIBUTOS DE NUESTRA CLASE
    #ES SIMILAR AL COMPUTE DE ODOO
    #QUE ES UN CONSTRUCTOR????????????????????????????????????????????

    #calcular retraso
    @property
    def dias_retraso(self):
        hoy = timezone.now().date() #el timezone now nos va a dar la fecha con zona horaria y todo, y el .date la fecha nomas
        #POR QUE USAMOS LOS 2?????????????????????????????????
        fecha_ref = hoy#pondra de fecha de referencia la fecha de devolucion o la de hoy, segun cual exista, si hay la devolucion
        #no usara la de hoy, si no hay usara hoy pq va en ordeen
        if fecha_ref > self.fecha_maxima: #si la fecha de referencia es mayor a la maxima
            return (fecha_ref - self.fecha_maxima).days #va a devolver los dias extras que se ha pasado con respeto a la fecha maxima
        #entender la logica,  pq se resta??
        return 0

    #ahora la de calcular la multa
    @property
    def multa_retraso(self):
        tarifa = 0.50
        return self.dias_retraso * tarifa #multiplica los dias de retraso por la tarifa diaria para calcular
    
    #la funcion del dias retraso esta creando un atributo a traves de una funcion, osea a pesar de ser una funcion es un
    #atributo propio de la funcion, por eso lo podemos llamar, dias retraso se convierte en un atributo, asi que no tenemos que hacer
    #compute o meterlo dentro de otro atributo, bacansisimo
    #@property aca no sirve property pq propety no puede guardar cosas en la base de datos, solo como que en una memoria temporal, para calculos
    def save(self, *args, **kwargs): #para fecha_maxima y fecha de devolucion
        dias = 7
        hoy = timezone.now().date() #date paa que solo saque fecha y no hora
        fecha_prestamos_date = None
        if isinstance(self.fecha_prestamos, str): #in in stance, revisa que fecha prestamos sea un string
            try: #intentara lo siguiente
                fecha_prestamos_date = datetime.strptime(self.fecha_prestamos, '%Y-%m-%d').date() #strptime es string parse time, agarra una cadena
                #(el fecha _prestamos) y la trata como si tuviera el formato de '%m-%d-%y' que es el que usan los gringos feos
                #con punto date quitamos la hora, solo fecha
            except: #si essto por algun motivo falla (pq ya es tipo date o ya esta grabado en la base de datos, no deberia pasar nunca pero por si acaso)
                pass
    
                #has attr revisa si el objeto tiene cierto atributo o metodo, en este caso revisa que fecha_prestamos sea tipo date, si no es tipo date
                #agarra la fecha asi nomas si ya es date o no necesita el .date
        fecha_ref = fecha_prestamos_date if fecha_prestamos_date else hoy
        #esto tambien se puede simplificar a:
        #fecha_ref = self.fecha_prestamos.date() if self.fecha_prestamos else timezone.now().date()
        if not self.fecha_maxima:
            self.fecha_maxima = fecha_ref + timedelta(days=dias) #time delta apara sumar dias para que sepa que son dias
        super().save(*args, **kwargs) #llamamos al metodo originar de save

        


    
    #AHORA EL TEMA DE LA MULTA
    
class multa(models.Model):
    prestamo= models.ForeignKey(Prestamo, related_name="multas", on_delete=models.PROTECT)
    tipo = models.CharField(max_length=10, choices=(
        ('r', 'retraso'), #clave valor
        ('p', 'perdida'),
        ('d', 'deterioro')
    ))#con choices definimos las opciones que tendra, al igual que odoo se debe definir ocn una tupla
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0) #decimal field es como el float, decimal_places es para ver cuantos decimales puede tener
    pagado = models.BooleanField(default=False) #para ver si esta pagado o no pagado
    fecha = models.DateField(default=timezone.now) #fecha a la que se crea la multa ,por defecto la fecha actual

    def __str__(self):
        return f"Multa {self.tipo} - {self.monto} - {self.prestamo}"
    
    #y al igual que odoo nosotros podemos redefinir algunas fucniones
    #vamos a redefinir la funcion save
    #QUE ES REDEFINIR??????????????????????????????????????
    def save(self, *args, **kwargs): #que es args y kwgars????
        if self.tipo == 'r' and self.monto == 0: #cuales deberian estar aca
            self.monto = self.prestamo.multa_retraso #como esta en prestamo hay que acceder asi
        super().save(*args, **kwargs) ##QUE HACE EL SUPER??? el super como la funcion save es una funcion propia de django, y la estamso reescribiendo, el super lo que va a
        #hacer es llamar a la funcion padre, o original y ejecutarla, entonces lo que hace es que aparte de lo que definimos nosotros va a usar la funcion
        #original
        #EXPLICAR ESTA FUNCION?????????????????????????????????????????????????????????