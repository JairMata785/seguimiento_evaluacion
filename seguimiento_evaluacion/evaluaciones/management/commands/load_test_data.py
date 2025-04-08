from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from evaluaciones.models import Carrera, Docente, Materia, Estudiante

class Command(BaseCommand):
    help = 'Carga datos de prueba para el sistema'

    def handle(self, *args, **kwargs):
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Materia.objects.all().delete()
        Estudiante.objects.all().delete()
        Docente.objects.all().delete()
        Carrera.objects.all().delete()
        get_user_model().objects.all().delete()

        User = get_user_model()

        # Create careers
        self.stdout.write('Creating careers...')
        sistemas = Carrera.objects.create(nombre='Ingeniería en Sistemas Computacionales')
        informatica = Carrera.objects.create(nombre='Ingeniería en Informática')

        # Create department head
        self.stdout.write('Creating department head...')
        jefe = User.objects.create_user(
            username='eva.platas',
            password='eva1234',
            first_name='Eva',
            last_name='Platas',
            user_type='department_head'
        )

        # Create teachers
        self.stdout.write('Creating teachers...')
        docentes_data = [
            # Informática teachers
            ('jose.infante', 'José Regino', 'Infante Aventura', 'D001', informatica),
            ('laura.chavez', 'Laura', 'Chavez', 'D002', informatica),
            ('marco.vazquez', 'Marco Antonio', 'Vazquez', 'D003', informatica),
        ]

        for username, nombre, apellido, num_emp, carrera in docentes_data:
            user = User.objects.create_user(
                username=username,
                password=f'{username.split(".")[0]}123',  # e.g., jose123
                first_name=nombre,
                last_name=apellido,
                user_type='teacher'
            )
            Docente.objects.create(
                user=user,
                numero_empleado=num_emp,
                carrera=carrera
            )

        # Create students
        self.stdout.write('Creating students...')
        estudiantes_data = [
            # Informática students
            ('jair.mata', 'Jair de Jesús', 'Mata Martínez', '20380598', informatica, 'jair123'),
            ('jorge.gonzalez', 'Jorge Luis', 'González Hernández', '20384058', informatica, 'jorg123'),
            ('uriel.dominguez', 'Angel Uriel', 'Domínguez Medina', '20380507', informatica, 'ange123'),
            # Sistemas student
            ('ana.guzman', 'Ana', 'Guzmán Elena', '2903849', sistemas, 'ana123'),
        ]

        for username, nombre, apellido, num_control, carrera, password in estudiantes_data:
            # First create the user
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=nombre,
                last_name=apellido,
                user_type='student'
            )
            # Then create the student profile with additional fields
            Estudiante.objects.create(
                user=user,
                numero_control=num_control,
                carrera=carrera
            )

        # Create subjects
        self.stdout.write('Creating subjects...')
        materias_data = [
            # Informática subjects
            ('INF101', 'Seguridad Informática', 'A', informatica),
            ('INF102', 'Gestión de TI', 'A', informatica),
            ('INF103', 'Cómputo en la Nube', 'A', informatica),
        ]

        # Assign subjects to teachers
        teacher_subject_mapping = {
            'jose.infante': 'Seguridad Informática',
            'laura.chavez': 'Gestión de TI',
            'marco.vazquez': 'Cómputo en la Nube',
        }

        for username, materia_nombre in teacher_subject_mapping.items():
            docente = Docente.objects.get(user__username=username)
            materia_data = next(m for m in materias_data if m[1] == materia_nombre)
            Materia.objects.create(
                clave=materia_data[0],
                nombre=materia_data[1],
                docente=docente,
                grupo=materia_data[2]
            )

        self.stdout.write(self.style.SUCCESS('Test data loaded successfully'))