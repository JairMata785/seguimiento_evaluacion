from django.shortcuts import render
from django.db.models import Avg
from ..models import EvaluacionAlumno, EvaluacionDepartamental, AutoEvaluacion, Docente

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