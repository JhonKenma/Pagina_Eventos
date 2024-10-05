from django.db import models
from django.contrib.auth.models import User
# Modelo para Categoría
class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

# Modelo para Evento
class Evento(models.Model):
    nombrEvento = models.CharField(max_length=100)
    descripcion = models.TextField()
    fechaInicio = models.DateTimeField()
    fechaFin = models.DateTimeField()
    lugar = models.CharField(max_length=100)
    # Relación de categoría con la tabla independiente de Categoría
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    # Organizador como un campo de texto, no relacionado con el modelo User
    organizador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) 
    costo = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)  # Ej: Precio en USD
    estadoEvento = models.CharField(max_length=20, default='Pendiente')  # Pendiente, En Curso, Finalizado, Cancelado
    imagen = models.ImageField(upload_to='eventos/', null=True, blank=True)  # Campo para la imagen del evento
     
    def __str__(self):
        return self.nombrEvento

# Modelo para el registro de usuarios en eventos
class RegistroEvento(models.Model):
    # Relaciona el usuario registrado con el modelo de usuario por defecto
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)  
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    fechaRegistro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.username} registrado en {self.evento}'
