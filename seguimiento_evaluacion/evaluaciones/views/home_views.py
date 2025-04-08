from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.user.is_student:
        return redirect('lista_docentes')
    elif request.user.is_teacher:
        return redirect('dashboard_docente')
    elif request.user.is_department_head:
        return redirect('lista_docentes_departamento')
    return render(request, 'evaluaciones/home.html')