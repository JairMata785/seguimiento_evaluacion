from django.urls import path
from .views import docente_views, jefe_views, home_views

urlpatterns = [
    path('', home_views.home, name='home'),
    
    # Rutas de docentes
    path('docente/autoevaluacion/', docente_views.autoevaluacion, name='autoevaluacion'),
    path('docente/reporte/<int:evaluacion_id>/', docente_views.descargar_reporte, name='descargar_reporte'),
    path('docente/mis-evaluaciones/', docente_views.ver_mis_evaluaciones, name='ver_mis_evaluaciones'),
    path('lista-docentes/', home_views.lista_docentes, name='lista_docentes'),
    path('detalle-docente/<int:docente_id>/', home_views.detalle_docente, name='detalle_docente'),
    
    # Rutas de jefe departamental
    path('jefe/evaluacion/<int:docente_id>/', jefe_views.evaluacion_departamental, name='evaluacion_departamental'),
    path('jefe/evaluaciones/<int:docente_id>/', jefe_views.ver_evaluaciones_docente, name='ver_evaluaciones_docente'),
]