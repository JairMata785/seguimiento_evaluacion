from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.conf import settings
import os

def generate_evaluation_report(evaluacion, tipo):
    output_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"evaluacion_{tipo}_{evaluacion.docente.numero_empleado}_{evaluacion.fecha}.pdf"
    filepath = os.path.join(output_dir, filename)
    
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    
    # Title
    title = Paragraph(f"Reporte de Evaluación - {tipo}", styles['Heading1'])
    elements.append(title)
    elements.append(Spacer(1, 20))
    
    # Docente info
    docente_info = [
        ["Docente:", evaluacion.docente.user.get_full_name()],
        ["Número de Empleado:", evaluacion.docente.numero_empleado],
        ["Fecha:", evaluacion.fecha.strftime("%d/%m/%Y")]
    ]
    
    t = Table(docente_info)
    t.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('PADDING', (0, 0), (-1, -1), 6)
    ]))
    elements.append(t)
    elements.append(Spacer(1, 20))
    
    # Evaluation data
    if tipo == 'autoevaluacion':
        data = [
            ["Aspecto", "Calificación"],
            ["Docencia", str(evaluacion.docencia)],
            ["Tutoría", str(evaluacion.tutoria)],
            ["Gestión", str(evaluacion.gestion)],
            ["Resultado Global", str(evaluacion.resultado_global)]
        ]
    else:
        data = [
            ["Aspecto", "Calificación"],
            ["Formación Docente", str(evaluacion.formacion_docente)],
            ["Planeación y Evaluación", str(evaluacion.planeacion_evaluacion)],
            ["Estrategias Didácticas", str(evaluacion.estrategias_didacticas)],
            ["Asesoría a Estudiantes", str(evaluacion.asesoria_estudiantes)],
            ["Participación como Tutor", str(evaluacion.participacion_tutor)],
            ["Gestión Tutorial", str(evaluacion.gestion_tutorial)],
            ["Resultado Final", str(evaluacion.resultado_final)]
        ]
    
    t = Table(data)
    t.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('PADDING', (0, 0), (-1, -1), 6)
    ]))
    elements.append(t)
    
    doc.build(elements)
    return filepath