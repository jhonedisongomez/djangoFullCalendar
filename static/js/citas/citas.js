function consultarCita(){

	var getMedicos = document.getElementById('SelectMedico');
	var indexMedicos = getMedicos.selectedIndex;
	var idMedico = getMedicos.options[indexMedicos].value;

	var consultorio = document.getElementById('txtConsultorio').value;
	$('#calendar').fullCalendar( 'removeEvents');
	$.ajax({

	    type: 'get',
	    url: '/',
	    data:{'id_medico': idMedico, 'id_consultorio': consultorio, 'method':'consultar'},
	    success: function(response)
	    {
	      var existeCitas = response.existe_citas;
	      var mensaje = response.mensaje;
	      
	      if(existeCitas){

	      		var events = JSON.parse(response.citas);
	      		var getEvent = []


	      		for(x = 0; x < events.length;x++){

	      			date = events[x].fields.fecha_inicio;
	      			date_f = events[x].fields.fecha_fin;
	      			id = events[x].pk;
	      			event = {'id': id,'title': 'cita','start': date,'end':date_f };
	      			getEvent.push(event);
	      		}

		        $('#calendar').fullCalendar( 'removeEventSource', getEvent);
		        $('#calendar').fullCalendar( 'addEventSource', getEvent);  
		        $('#calendar').fullCalendar( 'rerenderEvents' )
		        $('#calendar').fullCalendar( 'refetchEvents' ); 

	      }else{
	      	alert(mensaje);
	        $('#calendar').fullCalendar( 'removeEvents');

	      	
	      }
	    }
	});

}

fecha_cita = "";

$(document).ready(function() {
		
	$('#calendar').fullCalendar({
		header: {
			left: 'prev,next today, month',
			center: 'title',
			right: 'agendaWeek'
		},

		dayClick: function(date, jsEvent, view) {

		        //alert('Clicked on: ' + date.format());
		        fecha_cita = date.format();
		        $('#modal').modal('show'); 


		        //alert('Coordinates: ' + jsEvent.pageX + ',' + jsEvent.pageY);
		        // change the day's background color just for fun
		        //$(this).css('background-color', 'red');

	    },

		eventClick: function(event) {
				//alert(event.id);
		        
		        
		        //$('#modal').modal('show'); 
		        // change the border color just for fun
		        //$(this).css('border-color', 'red');

		    },

		defaultDate: '2017-10-12',
		navLinks: true, // can click day/week names to navigate views
		editable: true,
		eventLimit: true, // allow "more" link when too many events
		events: [

		]


	});
	
});


function crearCita(){

	var getMedicos = document.getElementById('SelectMedico');
	var indexMedicos = getMedicos.selectedIndex;
	var idMedico = getMedicos.options[indexMedicos].value;
	var consultorio = document.getElementById('txtConsultorio').value;
	var fechaInicio = fecha_cita
	var csrftoken = document.getElementById("csrfmiddlewaretoken").value;
	var idPersona = document.getElementById('txtPersona').value


	$.ajax({

	    type: 'post',
	    url: '/',
	    data:{'id_medico': idMedico,
    		 'id_consultorio': consultorio,
    		 'fecha_inicio':fechaInicio,
    		  'method':'crear',
    		  'id_persona': idPersona,
    		  'csrfmiddlewaretoken': csrftoken},
	    
	    success: function(response)
	    {
	    	alert(response.mensaje);
	    	consultarCita();
	    }
	});	

}



