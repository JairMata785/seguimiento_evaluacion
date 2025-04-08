from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from ..models import Docente, EvaluacionDepartamental, EvaluacionAlumno, AutoEvaluacion
from django.contrib import messages
from django.db.models import Avg

def is_department_head(user):
    return user.is_department_head

@login_required
@user_passes_test(is_department_head)
def lista_docentes_departamento(request):
    docentes = Docente.objects.all()
    return render(request, 'evaluaciones/jefe/lista_docentes.html', {'docentes': docentes})

@login_required
@user_passes_test(is_department_head)
def evaluacion_departamental(request, docente_id):
    docente = Docente.objects.get(id=docente_id)
    if request.method == 'POST':
        try:
            # Get all evaluation fields
            formacion_docente = float(request.POST.get('formacion_docente'))
            planeacion_evaluacion = float(request.POST.get('planeacion_evaluacion'))
            estrategias_didacticas = float(request.POST.get('estrategias_didacticas'))
            asesoria_estudiantes = float(request.POST.get('asesoria_estudiantes'))
            participacion_tutor = float(request.POST.get('participacion_tutor'))
            gestion_tutorial = float(request.POST.get('gestion_tutorial'))
            
            # Calculate final result as average
            resultado_final = (
                formacion_docente + 
                planeacion_evaluacion + 
                estrategias_didacticas + 
                asesoria_estudiantes + 
                participacion_tutor + 
                gestion_tutorial
            ) / 6
            
            evaluacion = EvaluacionDepartamental(
                docente=docente,
                formacion_docente=formacion_docente,
                planeacion_evaluacion=planeacion_evaluacion,
                estrategias_didacticas=estrategias_didacticas,
                asesoria_estudiantes=asesoria_estudiantes,
                participacion_tutor=participacion_tutor,
                gestion_tutorial=gestion_tutorial,
                resultado_final=resultado_final
            )
            evaluacion.save()
            messages.success(request, 'Evaluación guardada exitosamente')
            return redirect('lista_docentes_departamento')
        except ValueError:
            messages.error(request, 'Por favor, asegúrese de completar todos los campos correctamente')
        except Exception as e:
            messages.error(request, f'Error al guardar la evaluación: {str(e)}')
    
    return render(request, 'evaluaciones/jefe/evaluacion_form.html', {'docente': docente})


@login_required
@user_passes_test(is_department_head)
def ver_evaluaciones_docente(request, docente_id):
    docente = Docente.objects.get(id=docente_id)
    
    # Get all types of evaluations
    evaluaciones_departamentales = EvaluacionDepartamental.objects.filter(docente=docente)
    evaluaciones_alumnos = EvaluacionAlumno.objects.filter(docente=docente)
    autoevaluaciones = AutoEvaluacion.objects.filter(docente=docente)
    
    # Calculate averages
    promedio_departamental = evaluaciones_departamentales.aggregate(Avg('resultado_final'))
    promedio_alumnos = evaluaciones_alumnos.aggregate(Avg('satisfaccion_general'))
    promedio_auto = autoevaluaciones.aggregate(Avg('resultado_global'))
    
    context = {
        'docente': docente,
        'evaluaciones_departamentales': evaluaciones_departamentales,
        'evaluaciones_alumnos': evaluaciones_alumnos,
        'autoevaluaciones': autoevaluaciones,
        'promedios': {
            'departamental': promedio_departamental['resultado_final__avg'],
            'alumnos': promedio_alumnos['satisfaccion_general__avg'],
            'auto': promedio_auto['resultado_global__avg']
        }
    }
    
    return render(request, 'evaluaciones/jefe/ver_evaluaciones.html', context)