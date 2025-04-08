from django.urls import path
from .views import (
    home_views, auth_views, alumno_views, 
    docente_views, jefe_views
)
from .views import alumno_views

urlpatterns = [
    path('', home_views.home, name='home'),
    path('login/', auth_views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.CustomLogoutView.as_view(), name='logout'),
    
    # Student routes
    path('alumno/docentes/', alumno_views.lista_docentes, name='lista_docentes'),
    path('alumno/evaluacion/<int:docente_id>/<int:materia_id>/', 
         alumno_views.evaluacion_docente, name='evaluacion_docente'),
    
    # Department head routes
    path('jefe/docentes/', jefe_views.lista_docentes_departamento, 
         name='lista_docentes_departamento'),
    path('jefe/evaluacion/<int:docente_id>/', 
         jefe_views.evaluacion_departamental, name='evaluacion_departamental'),
    path('jefe/evaluaciones/<int:docente_id>/', 
         jefe_views.ver_evaluaciones_docente, name='ver_evaluaciones_docente'),
    
    # Teacher routes
    path('docente/dashboard/', docente_views.dashboard_docente, name='dashboard_docente'),
    path('docente/autoevaluacion/', docente_views.autoevaluacion, name='autoevaluacion'),
    path('docente/reporte/<int:evaluacion_id>/', 
         docente_views.descargar_reporte, name='descargar_reporte'),
    path('docente/mis-evaluaciones/', 
         docente_views.ver_mis_evaluaciones, name='ver_mis_evaluaciones'),
]