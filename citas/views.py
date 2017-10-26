from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView
from django.template import RequestContext
from django.http import HttpResponse
import json
from .models import *
from django.core import serializers
from datetime import datetime, timedelta

class CitasView(TemplateView):

    template_name = 'citas/citas.html'
    class_form = ''
    dic = {}
    response_data = {}
    def get(self, request, *args, **kwargs):

        

        if "method" in request.GET:
            method = request.GET['method']
            if method == 'consultar':

                id_medico = request.GET['id_medico']
                obj_medico = Medicos.objects.filter(id= id_medico)

                id_consultorio = request.GET['id_consultorio']
                obj_consultorio = Consultorio.objects.filter(id=id_consultorio)

                obj_cita = Cita.objects.filter(medico = obj_medico, consultorio=obj_consultorio)
                
                if obj_cita:
                    citas = serializers.serialize('json', obj_cita)
                    self.response_data['citas'] = citas
                    self.response_data['mensaje'] = 'existe citas'
                    self.response_data['existe_citas'] = True
                else:
                    self.response_data['mensaje'] = 'No existen citas'
                    self.response_data['existe_citas'] = False

                response_json = json.dumps(self.response_data)
                content_type = 'application/json'
                return HttpResponse(response_json, content_type)
        else:

            obj_medicos = Medicos.objects.all()
            self.dic = {'medicos':obj_medicos}
            context_instance = RequestContext(request)
            template = self.template_name
            return render_to_response(template, self.dic,context_instance)   
                
    def post(self, request, *args, **kwargs):

        method = request.POST['method']
        print request.POST
        if method == "crear":

            fecha_inicio  = request.POST['fecha_inicio']
            id_consultorio = request.POST['id_consultorio']
            obj_validar_cita = Cita.objects.filter(fecha_inicio = fecha_inicio, consultorio=id_consultorio)

            if obj_validar_cita:

                self.response_data['mensaje'] = "Ya esta separado la cita en este consultorio"
                
            
            else:

                id_medico = request.POST['id_medico']
                obj_medico = Medicos.objects.filter(id= id_medico)

                
                obj_consultorio = Consultorio.objects.filter(id=id_consultorio)      
                
                id_persona = request.POST['id_persona']
                obj_persona = Persona.objects.filter(identificacion= id_persona)


                date = datetime.strptime(fecha_inicio,'%Y-%m-%dT%H:%M:%S')
                date = date + timedelta(minutes=15)

                obj_nueva_cita = Cita()
                obj_nueva_cita.consultorio = obj_consultorio[0]
                obj_nueva_cita.persona = obj_persona[0]
                obj_nueva_cita.medico = obj_medico[0]
                obj_nueva_cita.fecha_inicio = fecha_inicio
                obj_nueva_cita.fecha_fin = date
                obj_nueva_cita.save()
                self.response_data['mensaje'] = "se guardo la nueva cita"
                

                
            response_json = json.dumps(self.response_data)
            content_type = 'application/json'
            return HttpResponse(response_json, content_type)