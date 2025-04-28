from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from evaluaciones.models import Carrera, Docente, Materia, Estudiante, EvaluacionAlumno, EvaluacionDepartamental, AutoEvaluacion
from decimal import Decimal
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Carga datos de prueba para el sistema'

    def handle(self, *args, **kwargs):
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        EvaluacionAlumno.objects.all().delete()
        EvaluacionDepartamental.objects.all().delete()
        AutoEvaluacion.objects.all().delete()
        Materia.objects.all().delete()
        Estudiante.objects.all().delete()
        Docente.objects.all().delete()
        Carrera.objects.all().delete()
        get_user_model().objects.all().delete()

        # Create careers
        self.stdout.write('Creating careers...')
        sistemas = Carrera.objects.create(nombre='Ingeniería en Sistemas Computacionales')
        informatica = Carrera.objects.create(nombre='Ingeniería en Informática')

        # Create teachers with extended information
        self.stdout.write('Creating teachers...')
        User = get_user_model()
        docentes_data = [
            # Informática teachers
            ('jose.infante', 'José Regino', 'Infante Aventura', 'D001', 'INIA781209ABC', informatica),
            ('laura.chavez', 'Laura', 'Chavez', 'D002', 'CHAL850315XYZ', informatica),
            ('marco.vazquez', 'Marco Antonio', 'Vazquez', 'D003', 'VAMA790622DEF', informatica),
            ('ana.martinez', 'Ana', 'Martínez López', 'D004', 'MALA800430GHI', sistemas),
            ('carlos.rodriguez', 'Carlos', 'Rodríguez Sánchez', 'D005', 'ROSC760815JKL', sistemas),
            ('patricia.gomez', 'Patricia', 'Gómez Torres', 'D006', 'GOTP820925MNO', informatica),
        ]

        docentes_creados = []
        for username, nombre, apellido, num_emp, rfc, carrera in docentes_data:
            # First create the user
            user = User.objects.create_user(
                username=username,
                password=f'{username}123',
                first_name=nombre,
                last_name=apellido,
                user_type='teacher'
            )
            # Then create the docente with the user
            docente = Docente.objects.create(
                user=user,
                numero_empleado=num_emp,
                rfc=rfc,
                carrera=carrera
            )
            docentes_creados.append(docente)

        # Create subjects
        self.stdout.write('Creating subjects...')
        materias_data = [
            ('INF101', 'Seguridad Informática', 'A', informatica),
            ('INF102', 'Gestión de TI', 'A', informatica),
            ('INF103', 'Cómputo en la Nube', 'A', informatica),
            ('SIS101', 'Programación Avanzada', 'A', sistemas),
            ('SIS102', 'Bases de Datos', 'B', sistemas),
            ('INF104', 'Inteligencia Artificial', 'B', informatica),
        ]

        materias_creadas = []
        # Assign subjects to teachers
        for i, (clave, nombre, grupo, carrera) in enumerate(materias_data):
            docente = docentes_creados[i % len(docentes_creados)]
            materia = Materia.objects.create(
                clave=clave,
                nombre=nombre,
                grupo=grupo,
                docente=docente
            )
            materias_creadas.append(materia)

        # Create students
        self.stdout.write('Creating students...')
        estudiantes_data = [
            ('juan.perez', 'Juan', 'Pérez', '2020123456', sistemas),
            ('maria.garcia', 'María', 'García', '2020123457', sistemas),
            ('pedro.lopez', 'Pedro', 'López', '2020123458', informatica),
            ('ana.martinez.est', 'Ana', 'Martínez', '2020123459', informatica),  # Cambiado el username
            ('luis.rodriguez', 'Luis', 'Rodríguez', '2020123460', sistemas),
        ]

        estudiantes_creados = []
        for username, nombre, apellido, num_control, carrera in estudiantes_data:
            user = User.objects.create_user(
                username=username,
                password=f'{username}123',
                first_name=nombre,
                last_name=apellido,
                user_type='student'
            )
            estudiante = Estudiante.objects.create(
                user=user,
                numero_control=num_control,
                carrera=carrera
            )
            estudiantes_creados.append(estudiante)

        # Create evaluaciones alumno
        self.stdout.write('Creating student evaluations...')
        for estudiante in estudiantes_creados:
            for materia in materias_creadas:
                if estudiante.carrera == materia.docente.carrera:
                    EvaluacionAlumno.objects.create(
                        estudiante=estudiante,
                        docente=materia.docente,
                        materia=materia,
                        dominio_asignatura=Decimal('4.50'),
                        planificacion_curso=Decimal('4.20'),
                        ambientes_aprendizaje=Decimal('4.30'),
                        estrategias_tecnicas=Decimal('4.40'),
                        motivacion=Decimal('4.60'),
                        evaluacion=Decimal('4.30'),
                        comunicacion=Decimal('4.50'),
                        gestion_curso=Decimal('4.40'),
                        tecnologias_informacion=Decimal('4.50'),
                        satisfaccion_general=Decimal('4.40')
                    )

        # Create evaluaciones departamentales
        self.stdout.write('Creating departmental evaluations...')
        for docente in docentes_creados:
            EvaluacionDepartamental.objects.create(
                docente=docente,
                formacion_docente=4,
                planeacion_evaluacion=5,
                estrategias_didacticas=4,
                asesoria_estudiantes=5,
                participacion_tutor=4,
                gestion_tutorial=5,
                resultado_final=Decimal('4.50')
            )

        # Create autoevaluaciones
        self.stdout.write('Creating self-evaluations...')
        for docente in docentes_creados:
            AutoEvaluacion.objects.create(
                docente=docente,
                docencia=Decimal('4.50'),
                tutoria=Decimal('4.30'),
                gestion=Decimal('4.40'),
                investigacion=Decimal('4.20'),
                vinculacion=Decimal('4.30')
            )

        self.stdout.write(self.style.SUCCESS('Test data loaded successfully'))