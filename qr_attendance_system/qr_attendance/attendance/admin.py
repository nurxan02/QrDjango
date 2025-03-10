from django.contrib import admin
from .models import Employee, Attendance

class AttendanceAdmin(admin.TabularInline):
    model = Attendance
    extra = 0 
    fields = ['check_in', 'check_out'] 

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'qr_code']
    inlines = [AttendanceAdmin]

