#TEST PERO APARA LAS VISTAS
from django.urls import reverse #nos sirve
from django.test import TestCase #explicar bien que hace el testcase, explicar bien el pillow tambien
from gestion.models import Libro, Autor


class Lista_Libro_ViewTest(TestCase):
    @classmethod
    def setUpTestData(cls): #siempre debe ser test data para que sirva los datos
        autor = Autor.objects.create(nombre='autor', apellido = 'libro', bibliografia='BBBBBBBBB')
        for i in range(3):
            Libro.objects.create(titulo=f"I Robot{i}", autor=autor, disponible=True)

    def test_url_existencias(self):
    #LA CLASE CLIENT SIMULA SER UN CLIENTE DE LA PAGINA WEB, ES DECIR VA A DAR UN GET DE LA URL, DA GET GET GET GET GET
        resp = self.client.get(reverse('lista_libros')) #QUE HACE EL REVERSE? EXPLICAR
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'gestion/templates/libros.html')
        self.assertEqual(len(resp.context['libros']), 3) #EXPLICAE ESTO TAMBIEN, EL RESP..CONTEXT

        #EXPLCIAR QUE HACE CADA ASSERT
        #da un error de que lista libro views no tieene atributo cls atomics
        #como arreglamos eso?
        #arreglar los fallos y entender esto de los test que esta bien util
