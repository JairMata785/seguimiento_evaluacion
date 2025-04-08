from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Estudiante'),
        ('teacher', 'Docente'),
        ('department_head', 'Jefe de Departamento'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    @property
    def is_student(self):
        return self.user_type == 'student'

    @property
    def is_teacher(self):
        return self.user_type == 'teacher'

    @property
    def is_department_head(self):
        return self.user_type == 'department_head'

class Carrera(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    
class Docente(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    numero_empleado = models.CharField(max_length=10)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.numero_empleado}"

class Materia(models.Model):
    clave = models.CharField(max_length=10)
    nombre = models.CharField(max_length=200)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    grupo = models.CharField(max_length=10)

class EvaluacionAlumno(models.Model):
    estudiante = models.ForeignKey('Estudiante', on_delete=models.CASCADE, null=True)
    docente = models.ForeignKey('Docente', on_delete=models.CASCADE)
    materia = models.ForeignKey('Materia', on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    
    dominio_asignatura = models.DecimalField(max_digits=3, decimal_places=2)
    planificacion_curso = models.DecimalField(max_digits=3, decimal_places=2)
    ambientes_aprendizaje = models.DecimalField(max_digits=3, decimal_places=2)
    estrategias_tecnicas = models.DecimalField(max_digits=3, decimal_places=2)
    motivacion = models.DecimalField(max_digits=3, decimal_places=2)
    evaluacion = models.DecimalField(max_digits=3, decimal_places=2)
    comunicacion = models.DecimalField(max_digits=3, decimal_places=2)
    gestion_curso = models.DecimalField(max_digits=3, decimal_places=2)
    tecnologias_informacion = models.DecimalField(max_digits=3, decimal_places=2)
    satisfaccion_general = models.DecimalField(max_digits=3, decimal_places=2)

class EvaluacionDepartamental(models.Model):
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    
    formacion_docente = models.IntegerField()
    planeacion_evaluacion = models.IntegerField()
    estrategias_didacticas = models.IntegerField()
    asesoria_estudiantes = models.IntegerField()
    participacion_tutor = models.IntegerField()
    gestion_tutorial = models.IntegerField()
    
    resultado_final = models.DecimalField(max_digits=3, decimal_places=2)
    
class AutoEvaluacion(models.Model):
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    
    docencia = models.DecimalField(max_digits=3, decimal_places=2)
    tutoria = models.DecimalField(max_digits=3, decimal_places=2)
    gestion = models.DecimalField(max_digits=3, decimal_places=2)
    investigacion = models.DecimalField(max_digits=3, decimal_places=2)
    vinculacion = models.DecimalField(max_digits=3, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.resultado_global = (float(self.docencia) + 
                               float(self.tutoria) + 
                               float(self.gestion) +
                               float(self.investigacion) +
                               float(self.vinculacion)) / 5
        super().save(*args, **kwargs)
    
    resultado_global = models.DecimalField(max_digits=3, decimal_places=2)

class Estudiante(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # Changed to CustomUser
    numero_control = models.CharField(max_length=10, unique=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.numero_control}"
