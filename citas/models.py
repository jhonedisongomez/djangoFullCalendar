# -*- coding: utf-8 -*-
from model_utils.models import TimeStampedModel
from django.db import models
from django.contrib.auth.models import User
from hospitalcloud import settings
from django.utils import timezone
import re
from datetime import date
from django_countries.fields import CountryField

class Persona(TimeStampedModel):
    """
    Representación de una :class:`Persona` en la aplicación
    Contiene los datos básicos que se utilizan para registar los datos de
    personas reales que se ingresan a la aplicación y de esta manera poder
    relacionarlos con el resto de las actividades que se realizan en la misma.
    """
    class Meta:
        permissions = (
        ('persona', 'Permite al usuario gestionar persona'),
        )
        ordering = ('created',)
    GENEROS = (
        ('M', ('Masculino')),
        ('F', ('Femenino')),
    )
    ESTADOS_CIVILES = (
        ('S', ('Soltero/a')),
        ('D', ('Divorciado/a')),
        ('C', ('Casado/a')),
        ('U', ('Union Libre')),
        ('', ('---------'))
    )
    TIPOS_IDENTIDAD = (
        ("R", ("Carnet de Residencia")),
        ("L", ("Licencia")),
        ("P", ("Pasaporte")),
        ("T", ("Tarjeta de Identidad")),
        ("N", ("Ninguno")),
    )
    __expresion__ = re.compile(r'\d{4}-\d{4}-\d{5}')
    tipo_identificacion = models.CharField(max_length=1,choices=TIPOS_IDENTIDAD, blank=True)
    identificacion = models.CharField(max_length=20, blank=True, unique=False)
    nombre = models.CharField(max_length=50, blank=True)
    apellido = models.CharField(max_length=50, blank=True)
    sexo = models.CharField(max_length=1, choices=GENEROS, blank=True)
    nacimiento = models.DateField(default=date.today)
    estado_civil = models.CharField(max_length=1, choices=ESTADOS_CIVILES,blank=True)
    profesion = models.CharField(max_length=200, blank=True)
    cargo = models.CharField(max_length=50, blank=True)
    telefono = models.CharField(max_length=200, blank=True)
    celular = models.CharField(max_length=200, blank=True)
    domicilio = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=200, blank=True)
    fax = models.CharField(max_length=200, blank=True)
    fotografia = models.ImageField(upload_to='persona/foto//%Y/%m/%d',blank=True, null=True,
    help_text="El archivo debe estar en "
    "formato jpg o png y no pesar "
    "mas de 120kb")
    nacionalidad = CountryField(blank=True)
    duplicado = models.BooleanField(default=False)
    rtn = models.CharField(max_length=200, blank=True, null=True)
    mostrar_en_cardex = models.BooleanField(default=False,verbose_name=("Es representante legal"))
    #ciudad = models.ForeignKey("users.Ciudad", blank=True, null=True)
    
    @staticmethod
    def validar_identidad(identidad):
        """Permite validar la identidad ingresada antes de asignarla a una
        :class:`Persona`
        :param identidad: Número de identidad a validar
        """
        return Persona.__expresion__.match(identidad)
    
    def __str__(self):
        """Muestra el nombre completo de la persona"""
        return self.nombre_completo()
    
    def get_absolute_url(self):
        """Obtiene la URL absoluta"""
        return reverse('persona-view-id', args=[self.id])
    
    def nombre_completo(self):
        """Obtiene el nombre completo de la :class:`Persona`"""
        return _('{0} {1}').format(self.nombre, self.apellido).upper()
    
    def obtener_edad(self):
        """Obtiene la edad de la :class:`Persona`"""
        if self.nacimiento is None:
            return None
        today = date.today()
        born = self.nacimiento
        return today.year - born.year - (
        (today.month, today.day) < (born.month, born.day))



class Consultorio(TimeStampedModel):
    class Meta:
        permissions = (

            ('consultorio', 'Permite al usuario gestionar consultorios'),
            ('clinical_read',
            ('Permite que el usuario tenga acceso a los datos clínicos')),
            ('clinical_write',
            ('Permite que el usuario escriba a los datos clínicos')),
            ('clinical_manage',
            ('Permite que el usuario escriba a los datos clínicos')),
        )

        ordering = ['nombre',]
    nombre = models.CharField(max_length=50, blank=True, null=True)
    usuario = models.ForeignKey(User,related_name='consultorios')
    secretaria = models.ForeignKey(User,related_name='secretarias')
    #inventario = models.ForeignKey(Inventario, related_name='consultorios',blank=True, null=True)
    administradores = models.ManyToManyField(User,blank=True,related_name='consultorios_administrados')
    #localidad = models.ForeignKey(Localidad, related_name='consultorios',blank=True, null=True)
    #especialidad = models.ForeignKey(Especialidad, related_name='consultorios',blank=True, null=True)
    activo = models.BooleanField(default=True)
    especialista = models.BooleanField(default=False)
    horario_inicio = models.TimeField(default=timezone.now, null=True, blank=True)
    horario_fin = models.TimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        """Obtiene la URL absoluta"""
        return reverse('consultorio', args=[self.id])
    
    def consultas_remitidas(self):
        return Consulta.objects.filter(remitida=True, revisada=False)

class Cita(TimeStampedModel):
    """Permite registrar las posibles :class:`Personas`s que serán atendidas
    en una fecha determinada"""
    consultorio = models.ForeignKey(Consultorio, related_name='citas',blank=True, null=True)
    persona = models.ForeignKey(Persona, related_name='citas', blank=True,null=True)
    #tipo = models.ForeignKey(TipoConsulta, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True, default=timezone.now)
    ausente = models.BooleanField(default=False)
    atendida = models.BooleanField(default=False)
    
    def get_absolute_url(self):
        """Obtiene la URL absoluta"""
        return self.consultorio.get_absolute_url()
    
    def __str__(self):
        return '{0}'.format(self.persona.nombre_completo())
    
    """def to_espera(self):
        espera = Espera()
        espera.consultorio = self.consultorio
        espera.persona = self.persona
        self.atendida = True
        self.save()
        return espera"""

