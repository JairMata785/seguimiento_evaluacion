from django.shortcuts import render
from django.db.models import Avg
from ..models import EvaluacionAlumno, EvaluacionDepartamental, AutoEvaluacion, Docente, Periodo, Materia, Estudiante

def home(request):
    docentes = Docente.objects.all()
    evaluaciones = {
        'alumnos': EvaluacionAlumno.objects.all(),
        'departamentales': EvaluacionDepartamental.objects.all(),
        'autoevaluaciones': AutoEvaluacion.objects.all()
    }
    
    # Calcular promedios generales
    promedios = {
        'alumnos': evaluaciones['alumnos'].aggregate(Avg('satisfaccion_general'))['satisfaccion_general__avg'],
        'departamentales': evaluaciones['departamentales'].aggregate(Avg('resultado_final'))['resultado_final__avg'],
        'auto': evaluaciones['autoevaluaciones'].aggregate(Avg('resultado_global'))['resultado_global__avg']
    }
    
    return render(request, 'evaluaciones/home.html', {
        'docentes': docentes,
        'evaluaciones': evaluaciones,
        'promedios': promedios
    })


def lista_docentes(request):
    docentes = Docente.objects.all()
    return render(request, 'evaluaciones/lista_docentes.html', {
        'docentes': docentes
    })


def detalle_docente(request, docente_id):
    try:
        docente = Docente.objects.get(id=docente_id)
        try:
            periodo = Periodo.objects.get(activo=True)
        except Periodo.DoesNotExist:
            periodo = None
        semestre = "2024-1"
        
        # Obtener alumnos de las materias del docente
        materias = Materia.objects.filter(docente=docente)
        alumnos = Estudiante.objects.filter(evaluacionalumno__materia__in=materias).distinct()
        
        return render(request, 'evaluaciones/detalle_docente.html', {
            'docente': docente,
            'periodo': periodo,
            'semestre': semestre,
            'materias': materias,
            'alumnos': alumnos
        })
    except Docente.DoesNotExist:
        from django.shortcuts import redirect
        return redirect('lista_docentes')