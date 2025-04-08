from django.db.models import Avg
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import FileResponse
from ..models import AutoEvaluacion, EvaluacionDepartamental, EvaluacionAlumno
from ..utils.pdf_generator import generate_evaluation_report
from django.contrib import messages

def is_teacher(user):
    return user.is_teacher

@login_required
@user_passes_test(is_teacher)
def autoevaluacion(request):
    if request.method == 'POST':
        try:
            evaluacion = AutoEvaluacion(
                docente=request.user.docente,
                docencia=request.POST.get('docencia'),
                tutoria=request.POST.get('tutoria'),
                gestion=request.POST.get('gestion'),
                investigacion=request.POST.get('investigacion'),
                vinculacion=request.POST.get('vinculacion')
            )
            evaluacion.save()
            messages.success(request, '¡La autoevaluación se ha guardado exitosamente!')
            return redirect('dashboard_docente')  # This should redirect to /docente/dashboard/
        except Exception as e:
            messages.error(request, 'Ha ocurrido un error al guardar la autoevaluación')
            
    return render(request, 'evaluaciones/docente/autoevaluacion_form.html')

@login_required
@user_passes_test(is_teacher)
def dashboard_docente(request):
    # Get all types of evaluations
    autoevaluaciones = AutoEvaluacion.objects.filter(docente=request.user.docente)
    evaluaciones_departamentales = EvaluacionDepartamental.objects.filter(docente=request.user.docente)
    evaluaciones_alumnos = EvaluacionAlumno.objects.filter(docente=request.user.docente)
    
    # Apply date filters if provided
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    
    if fecha_inicio:
        autoevaluaciones = autoevaluaciones.filter(fecha__gte=fecha_inicio)
        evaluaciones_departamentales = evaluaciones_departamentales.filter(fecha__gte=fecha_inicio)
        evaluaciones_alumnos = evaluaciones_alumnos.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        autoevaluaciones = autoevaluaciones.filter(fecha__lte=fecha_fin)
        evaluaciones_departamentales = evaluaciones_departamentales.filter(fecha__lte=fecha_fin)
        evaluaciones_alumnos = evaluaciones_alumnos.filter(fecha__lte=fecha_fin)
    
    # Calculate averages
    promedio_auto = autoevaluaciones.aggregate(Avg('resultado_global'))
    promedio_departamental = evaluaciones_departamentales.aggregate(Avg('resultado_final'))
    promedio_alumnos = evaluaciones_alumnos.aggregate(Avg('satisfaccion_general'))
    
    context = {
        'autoevaluaciones': autoevaluaciones[:5],  # Last 5 evaluations
        'evaluaciones_departamentales': evaluaciones_departamentales[:5],
        'evaluaciones_alumnos': evaluaciones_alumnos[:5],
        'promedios': {
            'auto': promedio_auto['resultado_global__avg'],
            'departamental': promedio_departamental['resultado_final__avg'],
            'alumnos': promedio_alumnos['satisfaccion_general__avg']
        }
    }
    
    return render(request, 'evaluaciones/docente/dashboard.html', context)

@login_required
@user_passes_test(is_teacher)
def descargar_reporte(request, evaluacion_id):
    evaluacion = AutoEvaluacion.objects.get(id=evaluacion_id)
    filepath = generate_evaluation_report(evaluacion, 'autoevaluacion')
    return FileResponse(open(filepath, 'rb'), as_attachment=True)

@login_required
@user_passes_test(is_teacher)
def ver_mis_evaluaciones(request):
    evaluaciones_departamentales = EvaluacionDepartamental.objects.filter(docente=request.user.docente)
    evaluaciones_alumnos = EvaluacionAlumno.objects.filter(docente=request.user.docente)
    autoevaluaciones = AutoEvaluacion.objects.filter(docente=request.user.docente)
    
    # Calculate averages
    promedio_departamental = evaluaciones_departamentales.aggregate(Avg('resultado_final'))
    promedio_alumnos = evaluaciones_alumnos.aggregate(Avg('satisfaccion_general'))
    promedio_auto = autoevaluaciones.aggregate(Avg('resultado_global'))
    
    context = {
        'evaluaciones_departamentales': evaluaciones_departamentales,
        'evaluaciones_alumnos': evaluaciones_alumnos,
        'autoevaluaciones': autoevaluaciones,
        'promedios': {
            'departamental': promedio_departamental['resultado_final__avg'],
            'alumnos': promedio_alumnos['satisfaccion_general__avg'],
            'auto': promedio_auto['resultado_global__avg']
        }
    }
    
    return render(request, 'evaluaciones/docente/mis_evaluaciones.html', context)

@login_required
@user_passes_test(is_teacher)
def ver_evaluaciones_alumnos(request):
    evaluaciones = EvaluacionAlumno.objects.filter(docente=request.user.docente)
    
    # Calculate averages for each aspect
    promedios = {
        'dominio_asignatura': evaluaciones.aggregate(Avg('dominio_asignatura'))['dominio_asignatura__avg'] or 0,
        'planificacion_curso': evaluaciones.aggregate(Avg('planificacion_curso'))['planificacion_curso__avg'] or 0,
        'ambientes_aprendizaje': evaluaciones.aggregate(Avg('ambientes_aprendizaje'))['ambientes_aprendizaje__avg'] or 0,
        'estrategias_tecnicas': evaluaciones.aggregate(Avg('estrategias_tecnicas'))['estrategias_tecnicas__avg'] or 0,
        'motivacion': evaluaciones.aggregate(Avg('motivacion'))['motivacion__avg'] or 0,
        'evaluacion': evaluaciones.aggregate(Avg('evaluacion'))['evaluacion__avg'] or 0,
        'comunicacion': evaluaciones.aggregate(Avg('comunicacion'))['comunicacion__avg'] or 0,
        'gestion_curso': evaluaciones.aggregate(Avg('gestion_curso'))['gestion_curso__avg'] or 0,
        'tecnologias_informacion': evaluaciones.aggregate(Avg('tecnologias_informacion'))['tecnologias_informacion__avg'] or 0,
        'satisfaccion_general': evaluaciones.aggregate(Avg('satisfaccion_general'))['satisfaccion_general__avg'] or 0,
    }
    
    # Prepare data for template
    evaluation_aspects = [
        {'name': 'A) Dominio de la asignatura', 'score': promedios['dominio_asignatura']},
        {'name': 'B) Planificación del curso', 'score': promedios['planificacion_curso']},
        {'name': 'C) Ambientes de aprendizaje', 'score': promedios['ambientes_aprendizaje']},
        {'name': 'D) Estrategias, métodos y técnicas', 'score': promedios['estrategias_tecnicas']},
        {'name': 'E) Motivación', 'score': promedios['motivacion']},
        {'name': 'F) Evaluación', 'score': promedios['evaluacion']},
        {'name': 'G) Comunicación', 'score': promedios['comunicacion']},
        {'name': 'H) Gestión del curso', 'score': promedios['gestion_curso']},
        {'name': 'I) Tecnologías de la información', 'score': promedios['tecnologias_informacion']},
        {'name': 'J) Satisfacción general', 'score': promedios['satisfaccion_general']},
    ]
    
    # Add qualitative ratings
    for aspect in evaluation_aspects:
        aspect['rating'] = get_qualitative_rating(aspect['score'])
    
    # Calculate total
    total_score = sum(aspect['score'] for aspect in evaluation_aspects) / len(evaluation_aspects)
    
    context = {
        'evaluation_aspects': evaluation_aspects,
        'total_score': total_score,
        'total_rating': get_qualitative_rating(total_score),
        'aspect_labels': [aspect['name'] for aspect in evaluation_aspects],
        'aspect_scores': [aspect['score'] for aspect in evaluation_aspects],
        'evaluaciones': evaluaciones
    }
    
    return render(request, 'evaluaciones/docente/evaluaciones_alumnos.html', context)