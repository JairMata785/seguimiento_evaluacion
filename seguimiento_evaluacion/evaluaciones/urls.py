from django.urls import path
from .views import home_views, docente_views, jefe_views

urlpatterns = [
    path('', home_views.home, name='home'),
    
    # Rutas de docentes
    path('docente/autoevaluacion/', docente_views.autoevaluacion, name='autoevaluacion'),
    path('docente/reporte/<int:evaluacion_id>/', docente_views.descargar_reporte, name='descargar_reporte'),
    path('docente/mis-evaluaciones/', docente_views.ver_mis_evaluaciones, name='ver_mis_evaluaciones'),
    
    # Rutas de jefe departamental
    path('jefe/evaluacion/<int:docente_id>/', jefe_views.evaluacion_departamental, name='evaluacion_departamental'),
    path('jefe/evaluaciones/<int:docente_id>/', jefe_views.ver_evaluaciones_docente, name='ver_evaluaciones_docente'),
]