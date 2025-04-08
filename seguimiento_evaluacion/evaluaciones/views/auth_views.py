from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def get_success_url(self):
        user = self.request.user
        if user.is_student:
            return reverse_lazy('lista_docentes')
        elif user.is_teacher:
            return reverse_lazy('dashboard_docente')  # Make sure this matches the URL name
        elif user.is_department_head:
            return reverse_lazy('lista_docentes_departamento')
        return reverse_lazy('login')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # Using reverse_lazy here for consistency