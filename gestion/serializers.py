from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class AutorSerializer(serializers.ModelSerializer):
    total_libros = serializers.SerializerMethodField()
    class Meta:
        model = Autor
        fields = ['id', 'nombre', 'apellido']

    def get_total_libros(self, obj):
        return obj.libros.count()

class LibroSerializer(serializers.ModelSerializer):
    autor_nombre = serializers.CharField(source='autor.__str__', read_only=True) #necesitamos el nombre del autor para el libro

    class Meta:
        model = Libro
        fields = {'id', 'titulo', 'autor', 'disponible'}
        #si tuvieramos isbn  fields = {'id', 'titulo', 'autor', 'disponible', 'isbn'}
        #y deberiamos validar el isbn con
        ''' def validate_isbn(self, value)
                if len(value) not in [10, 13]:
                    raise serializers.ValidationError("ISBN debe tener 10 o 13 digitos")
                return value'''

class PrestamosSerializers():
    pass 