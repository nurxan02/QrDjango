from django.contrib import admin
from .models import Employee, Attendance

admin.site.register(Employee)
admin.site.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'check_in', 'check_out']