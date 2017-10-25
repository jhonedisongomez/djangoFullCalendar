@python_2_unicode_compatible
class Consultorio(TimeStampedModel):
     class Meta:
         permissions = (
             ('consultorio', 'Permite al usuario gestionar consultorios'),
             ('clinical_read',
             _('Permite que el usuario tenga acceso a los datos clínicos')),
             ('clinical_write',
             _('Permite que el usuario escriba a los datos clínicos')),
             ('clinical_manage',
             _('Permite que el usuario escriba a los datos clínicos')),
         )
    ordering = ["nombre", ]
    nombre = models.CharField(max_length=50, blank=True, null=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='consultorios')
    secretaria = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='secretarias')
    inventario = models.ForeignKey(Inventario, related_name='consultorios',blank=True, null=True)
    administradores = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='consultorios_administrados')
    localidad = models.ForeignKey(Localidad, related_name='consultorios',blank=True, null=True)
    especialidad = models.ForeignKey(Especialidad, related_name='consultorios',blank=True, null=True)
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

@python_2_unicode_compatible
class Cita(TimeStampedModel):
    """Permite registrar las posibles :class:`Personas`s que serán atendidas
    en una fecha determinada"""
    consultorio = models.ForeignKey(Consultorio, related_name='citas',blank=True, null=True)
    persona = models.ForeignKey(Persona, related_name='citas', blank=True,null=True)
    tipo = models.ForeignKey(TipoConsulta, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True, default=timezone.now)
    ausente = models.BooleanField(default=False)
    atendida = models.BooleanField(default=False)
    
    def get_absolute_url(self):
        """Obtiene la URL absoluta"""
        return self.consultorio.get_absolute_url()
    
    def __str__(self):
        return '{0}'.format(self.persona.nombre_completo())
    
    def to_espera(self):
        espera = Espera()
        espera.consultorio = self.consultorio
        espera.persona = self.persona
        self.atendida = True
        self.save()
        return espera