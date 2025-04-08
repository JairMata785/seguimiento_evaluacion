from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Docente, Estudiante, Materia, EvaluacionAlumno

@login_required
def lista_docentes(request):
    if not request.user.is_authenticated or not request.user.is_student:
        messages.error(request, 'Acceso no autorizado. Esta página es solo para estudiantes.')
        return render(request, 'evaluaciones/403.html', status=403)
        
    try:
        estudiante = Estudiante.objects.get(user=request.user)
        docentes = Docente.objects.filter(carrera=estudiante.carrera)
        
        docentes_data = []
        for docente in docentes:
            materias = Materia.objects.filter(docente=docente)
            
            for materia in materias:
                # Check if evaluation exists for this docente and materia combination
                evaluacion_existente = EvaluacionAlumno.objects.filter(
                    docente=docente,
                    materia=materia
                ).exists()
                
                docentes_data.append({
                    'docente': docente,
                    'materia': materia,
                    'evaluado': evaluacion_existente
                })
        
        return render(request, 'evaluaciones/alumno/lista_docentes.html', {
            'docentes_data': docentes_data
        })
        
    except Estudiante.DoesNotExist:
        messages.error(request, 'No se encontró el perfil de estudiante.')
        return render(request, 'evaluaciones/404.html', status=404)

@login_required
def evaluacion_docente(request, docente_id, materia_id):
    if request.method == 'POST':
        estudiante = Estudiante.objects.get(user=request.user)
        evaluacion = EvaluacionAlumno(
            estudiante=estudiante,
            docente_id=docente_id,
            materia_id=materia_id,
            dominio_asignatura=request.POST.get('dominio_asignatura'),
            planificacion_curso=request.POST.get('planificacion_curso'),
            ambientes_aprendizaje=request.POST.get('ambientes_aprendizaje'),
            estrategias_tecnicas=request.POST.get('estrategias_tecnicas'),
            motivacion=request.POST.get('motivacion'),
            evaluacion=request.POST.get('evaluacion'),
            comunicacion=request.POST.get('comunicacion'),
            gestion_curso=request.POST.get('gestion_curso'),
            tecnologias_informacion=request.POST.get('tecnologias_informacion'),
            satisfaccion_general=request.POST.get('satisfaccion_general')
        )
        evaluacion.save()
        return redirect('lista_docentes')
    
    docente = Docente.objects.get(id=docente_id)
    materia = Materia.objects.get(id=materia_id)
    return render(request, 'evaluaciones/alumno/evaluacion_form.html', {
        'docente': docente,
        'materia': materia
    })