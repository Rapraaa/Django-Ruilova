from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission 

#TODO bodeguero,bibliotecario,administrador,cliente 
#bibliotecario solo ver, prestar, prestamos,multas
#el cliente solicita el libro pero el bibliotecario es el que debe prestar
#bodeguero crear libros, crear autores
#que en perfil vera uqe grupo es
#el admin crea los usuarios y elige su grupo, una parte para crear los especiales
#que al usuario no le salga la pesta;a de autores directamente pq no va a poder verlos xd
@receiver(post_save, sender=User) #que se ejecute solo despues de que se guarde algo, con el sender le decimos que ese algo es un usuario
def dar_permisos(sender, instance, created, **kwargs): #SENDER = Quién envió la señal (La clase User)
    #instance: EL DATO CLAVE. Es el usuario específico que se acaba de crear (ej: "Juan Pérez")
    #created: Un semáforo (Verdadero o Falso). Nos dice: "¿este usuario se acaba de crear hoy o solo modifico algo?"
    #kwargs es como una bolsa que guarda cualquier otro dato que envie y que no necesitemos para evitar error, pq el psot save puede mandar mas cosas
    #por ejemplo si en alguna parte guardo en el usuario con un update fields se damiaria si no uso el kwargs
    if created: #si fue creado y no modificado
        try: #va a intentar esto
            grupo = Group.objects.get(name='Usuario') #saca en la variable grupos el grupo de usuario prestamos que cree desde admin

            instance.groups.add(grupo) #a la instancia (el usuario que se creo) le va a agregar ese grupo

        except Group.DoesNotExist: #si por algun motivo falla (que no deberia)
            pass #no hace nada xd