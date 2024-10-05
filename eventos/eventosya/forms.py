from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from .models import Evento
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone

class RegistroForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Cambia 'correo' a 'username' y 'contrasena' a 'password'
        widgets = {
            'password': forms.PasswordInput(),  # Asegúrate de que el campo de contraseña sea un input de tipo password
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Usa set_password para establecer la contraseña
        if commit:
            user.save()
        return user


# Formulario de Login usando el campo email y password
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())  # Widget para ocultar la contraseña



class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = [
            'nombrEvento', 
            'descripcion', 
            'fechaInicio', 
            'fechaFin', 
            'lugar', 
            'costo', 
            'categoria', 
            'imagen'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fechaInicio'].initial = timezone.now()
        self.fields['fechaInicio'].widget.attrs['readonly'] = 'readonly'