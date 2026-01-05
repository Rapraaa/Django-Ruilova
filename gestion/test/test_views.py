#TEST PERO APARA LAS VISTAS
from django.urls import reverse #nos sirve
from django.test import TestCase, Client #explicar bien que hace el testcase, explicar bien el pillow tambien y el client
from gestion.models import Libro, Autor
import json
from django.utils.decorators import patch


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

class LibrosViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url_crear = reverse('crear_libro') # Asegúrate que este nombre coincida con tu urls.py

    # Este "patch" intercepta la llamada a internet y devuelve lo que nosotros queramos
    @patch('requests.get')
    def test_buscar_libro_api_exito(self, mock_get):
        # Simulamos una respuesta exitosa de la API (Mock)
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "docs": [{
                "title": "Libro de Prueba",
                "author_name": ["Autor de Prueba"]
            }]
        }

        # Ejecutamos la búsqueda (GET)
        response = self.client.get(self.url_crear, {'busqueda': 'Libro de Prueba'})

        # Verificaciones:
        self.assertEqual(response.status_code, 200)
        self.assertIn('Libro de Prueba', response.context['datos_iniciales']['titulo'])
        # Verificamos que se creó el autor en la BD automáticamente
        self.assertTrue(Autor.objects.filter(nombre="Autor de").exists())

    def test_guardar_libro_post(self):
        # Primero necesitamos un autor en la BD para poder seleccionarlo
        autor = Autor.objects.create(nombre="Pepe", apellido="Perez")
        
        # Enviamos el formulario (POST)
        response = self.client.post(self.url_crear, {
            'titulo': 'Nuevo Libro Manual',
            'autor_id': autor.id
        })

        # Verificamos que nos redirija a la lista
        self.assertRedirects(response, reverse('lista_libros'))
        # Verificamos que el libro se creó de verdad
        self.assertEqual(Libro.objects.count(), 1)