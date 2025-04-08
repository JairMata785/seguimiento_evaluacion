from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Carrera, Docente, Materia, EvaluacionAlumno, EvaluacionDepartamental, AutoEvaluacion

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Tipo de Usuario', {'fields': ('user_type',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Tipo de Usuario', {'fields': ('user_type',)}),
    )

class DocenteAdmin(admin.ModelAdmin):
    list_display = ('numero_empleado', 'get_nombre_completo', 'carrera')
    list_filter = ('carrera',)
    search_fields = ('numero_empleado', 'user__first_name', 'user__last_name')

    def get_nombre_completo(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_nombre_completo.short_description = 'Nombre Completo'

class MateriaAdmin(admin.ModelAdmin):
    list_display = ('clave', 'nombre', 'docente', 'grupo')
    list_filter = ('docente__carrera',)
    search_fields = ('clave', 'nombre', 'grupo')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Carrera)
admin.site.register(Docente, DocenteAdmin)
admin.site.register(Materia, MateriaAdmin)
admin.site.register(EvaluacionAlumno)
admin.site.register(EvaluacionDepartamental)
admin.site.register(AutoEvaluacion)
